from django.template import defaultfilters
from django_cradmin.viewhelpers import objecttable
from django_cradmin import crapp
from django_cradmin import crinstance
from django.utils.translation import ugettext_lazy as _

from devilry.apps.core.models import AssignmentGroup
from devilry.devilry_student.cradminextensions import studentobjecttable


class AssignmentInfoColumn(objecttable.SingleActionColumn):
    orderingfield = 'parentnode__long_name'

    def render_value(self, group):
        return group.parentnode.long_name

    def get_header(self):
        return _('Assignment')

    def get_actionurl(self, group):
        return crinstance.reverse_cradmin_url(
            instanceid='devilry_student_group',
            appname='deliveries',
            roleid=group.id,
            viewname='add-delivery')


class PeriodInfoColumn(objecttable.PlainTextColumn):
    orderingfield = 'parentnode__parentnode__parentnode__long_name'

    def get_header(self):
        return _('Course')

    def render_value(self, group):
        return u'{} - {}'.format(
            group.subject.long_name,
            group.period.long_name)


class DeadlineColumn(objecttable.DatetimeColumn):
    orderingfield = 'parentnode__parentnode__parentnode__long_name'
    modelfield = 'last_deadline_datetime'

    def get_header(self):
        return _('Deadline')


class WaitingForDeliveriesListView(studentobjecttable.StudentObjectTableView):
    model = AssignmentGroup
    columns = [
        AssignmentInfoColumn,
        PeriodInfoColumn,
        DeadlineColumn
    ]

    def get_pagetitle(self):
        return _('Assignments open for delivery')

    def get_queryset_for_role(self, period):
        return AssignmentGroup.objects\
                .filter_student_has_access(self.request.user)\
                .filter_is_active()\
                .filter_waiting_for_deliveries()\
                .annotate_with_last_deadline_datetime()\
                .select_related(
                    'parentnode', # Assignment
                    'parentnode__parentnode', # Period
                    'parentnode__parentnode__parentnode', # Subject
                )


class App(crapp.App):
    appurls = [
        crapp.Url(
            r'^$',
            WaitingForDeliveriesListView.as_view(),
            name=crapp.INDEXVIEW_NAME),
    ]
