from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.i18n import javascript_catalog

from devilry.restful.forbidden import forbidden_if_not_authenticated
from restful import student_restful
from views import (MainView, AddDeliveryView,
                   FileUploadView, AssignmentGroupView,
                   FileDownloadView, ShowDeliveryView,
                   CompressedFileDownloadView)

i18n_packages = ('core',)

urlpatterns = patterns('devilry.apps.student',
                       url(r'^$', login_required(MainView.as_view()), name='student'),
                       url(r'^add-delivery/(?P<assignmentgroupid>\d+)$', 
                           login_required(AddDeliveryView.as_view()), 
                           name='add-delivery'),
                       url(r'^add-delivery/fileupload/(?P<assignmentgroupid>\d+)$',
                           forbidden_if_not_authenticated(FileUploadView.as_view()),
                           name='file-upload'),
                       url(r'^assignmentgroup/(?P<assignmentgroupid>\d+)$',
                           login_required(AssignmentGroupView.as_view()),
                           name='student-show-assignmentgroup'),
                       url(r'^show-delivery/(?P<deliveryid>\d+)$',
                           login_required(ShowDeliveryView.as_view()),
                           name='show-delivery'),
                       url(r'^show-delivery/filedownload/(?P<filemetaid>\d+)$',
                           login_required(FileDownloadView.as_view()),
                           name='file-download'),
                       url(r'^show-delivery/compressedfiledownload/(?P<deliveryid>\d+)$',
                           login_required(CompressedFileDownloadView.as_view()),
                           name='compressed-file-download'),
                       #url(r'^show-delivery/tarfiledownload/(?P<deliveryid>\d+)$',
                           #login_required(TarFileDownloadView.as_view()),
                           #name='tar-file-download'),
                       url('^i18n.js$', javascript_catalog,
                           kwargs={'packages': i18n_packages},
                           name='devilry_student_i18n')
                       )

urlpatterns += student_restful
