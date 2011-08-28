from django.views.generic import TemplateView, View
from django.shortcuts import render
from tempfile import TemporaryFile
from devilry.apps.gradeeditors.restful import examiner as gradeeditors_restful
from devilry.utils.module import dump_all_into_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from ..core.models import (Assignment)
from devilry.utils.filewrapperwithexplicitclose import FileWrapperWithExplicitClose
import zipfile
import tarfile
import os, glob
import shutil
import restful


class MainView(TemplateView):
    template_name='examiner/main.django.html'

    def get_context_data(self):
        context = super(MainView, self).get_context_data()
        context['restfulapi'] = dump_all_into_dict(restful);
        return context


class AssignmentGroupView(View):
    def get(self, request, assignmentgroupid):
        context = {'objectid': assignmentgroupid,
                   'restfulapi': dump_all_into_dict(restful),
                   'gradeeditors': dump_all_into_dict(gradeeditors_restful)
                  }
        return render(request,
                      'examiner/assignmentgroupview.django.html',
                       context)

class AssignmentView(View):
    def get(self, request, assignmentid):
        context = {'assignmentid': assignmentid,
                   'restfulapi': dump_all_into_dict(restful),
                   'gradeeditors': dump_all_into_dict(gradeeditors_restful)
                  }
        return render(request,
                      'examiner/assignment.django.html',
                       context) 

                       
class CompressedFileDownloadView(View):

    def _get_candidates_as_string(self, candidates, assignmentgroup_id):
        candidates_as_string = ""
        size = len(candidates)-1
        for candidate in candidates:
            candidates_as_string += str(candidate)
            if candidate == candidates[size]:
                candidates_as_string += "_"
            else:
                candidates_as_string += "-"
        candidates_as_string += str(assignmentgroup_id)
        return candidates_as_string

    def _add_directory_to_zipfile(self, zip_file, basedir):
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), "deliveries")):
            for fn in files:
                absolute_fn = os.path.join(root, fn)
                relative_fn = absolute_fn[len(basedir)+len(os.sep):]
                zip_file.write(absolute_fn, relative_fn)
        zip_file.close()

    def _copy_file_from_deliverystore(self, filemeta):
        file_content = filemeta.deliverystore.read_open(filemeta)
        ut = open(filemeta.filename, 'wb')
        for data in file_content:
            ut.write(data)
        ut.close()

    #TODO use temporary directory
    def get(self, request, assignmentid):
        assignment = get_object_or_404(Assignment, id=assignmentid)
        
        basedir = os.getcwd()
        os.mkdir("deliveries")
        os.chdir(os.path.join(os.getcwd(), "deliveries"))
        
        zip_file_name = assignment.short_name + ".zip"
        tempfile = TemporaryFile()
        zip_file = zipfile.ZipFile(tempfile, 'w');        
                
        for assignmentgroup in assignment.assignmentgroups.all():
            candidates = self._get_candidates_as_string(assignmentgroup.candidates.all(), assignmentgroup.id)
            
            for deadline in assignmentgroup.deadlines.all():
            
                deadline_dir = os.getcwd()
                deadline_dir_name = deadline.deadline.strftime("%d-%m-%Y_")
                deadline_dir_name += str(assignmentgroup.id)
                os.mkdir(deadline_dir_name)
                
                os.chdir(os.path.join(os.getcwd(), deadline_dir_name))
                os.mkdir(candidates)
                
                for delivery in deadline.deliveries.all():
                    delivery_dir = os.getcwd()
                    os.chdir(os.path.join(os.getcwd(), candidates))
                    os.mkdir(str(delivery.number))
                    os.chdir(os.path.join(os.getcwd(), str(delivery.number)))
                    
                    for filemeta in delivery.filemetas.all():                        
                        self._copy_file_from_deliverystore(filemeta)
                        
                    os.chdir(delivery_dir)                        
                os.chdir(deadline_dir)
        os.chdir(basedir)

        self._add_directory_to_zipfile(zip_file, basedir)
        shutil.rmtree(os.path.join(os.getcwd(), "deliveries"))

        tempfile.seek(0)
        response = HttpResponse(FileWrapperWithExplicitClose(tempfile),
                                content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename=%s" % \
            zip_file_name.encode("ascii", 'replace')
        response['Content-Length'] = os.stat(tempfile.name).st_size
        return response #HttpResponse("Hei Verden")
