from django.views.generic import ListView
from django.views.generic import TemplateView
from devilry.apps.core.models import Assignment
from devilry.apps.core.models import Period
from devilry_qualifiesforexam.models import Status

class SemesterOverview(ListView):
    """

    This view list every assignemnt of a period

    """
    template_name = "devilry_student/semesteroverview.django.html"
    model = Assignment
    paginate_by = 100

    def __init__(self):
        super(SemesterOverview, self).__init__()

    def get_context_data(self, *args, **kwargs):
        context = super(SemesterOverview, self).get_context_data(*args, **kwargs)
        period = Period.objects.get(id=self.kwargs['pk'])
        context['period'] = period
        context['qualifiesforexams'] = None
        try:
            status = Status.get_current_status(period)
        except Status.DoesNotExist:
            pass
        else:
            if status.status == Status.READY:
                try:
                    qualifies = status.students.get(relatedstudent__user=self.request.user)
                    context['qualifiesforexams'] = qualifies.qualifies
                except QualifiesForFinalExam.DoesNotExist:
                    pass
        return context

    def get_queryset(self):
        user = self.request.user
        period_id = self.kwargs['pk']
        queryset = Assignment.objects.filter_is_active().filter(parentnode__id=period_id).order_by('-publishing_time')
        return queryset