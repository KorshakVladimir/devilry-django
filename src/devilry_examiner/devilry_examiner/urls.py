from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

from django_decoupled_docs.registry import documentationregistry
from devilry_settings.docproxies import DevilryUserDocsProxy
from devilry_settings.i18n import get_javascript_catalog_packages
from .views.dashboard import DashboardView
from .views.singlegroupoverview import SingleGroupOverview
from .views.allgroupsoverview import AllGroupsOverview
from .views.allgroupsoverview import WaitingForFeedbackOverview
from .views.allgroupsoverview import WaitingForFeedbackOrAllRedirectView
from .views.allgroupsoverview import WaitingForDeliveriesOverview
from .views.allgroupsoverview import CorrectedOverview
from .views.singledelivery import SingleDeliveryView
from .views.add_deadline import AddDeadlineView
from .views.close_groups import CloseGroupsView
from .views.add_nonelectronic_delivery import AddNonElectronicDeliveryView
from .views.lastdelivery_or_groupoverview_redirect import LastDeliveryOrGroupOverviewRedirectView


urlpatterns = patterns('devilry_examiner',
    #url('^rest/', include('devilry_examiner.rest.urls')),
    url('^$', login_required(DashboardView.as_view()),
        name='devilry_examiner_dashboard'),
    url('^allgroupsoverview/(?P<assignmentid>\d+)$',
        login_required(AllGroupsOverview.as_view()),
        name='devilry_examiner_allgroupsoverview'),
    url('^allgroupsoverview/(?P<assignmentid>\d+)/waiting_for_feedback$',
        login_required(
            WaitingForFeedbackOverview.as_view()),
        name='devilry_examiner_waiting_for_feedback'),
    url('^allgroupsoverview/(?P<assignmentid>\d+)/waiting_for_feedback_or_all$',
        login_required(WaitingForFeedbackOrAllRedirectView.as_view()),
        name='devilry_examiner_waiting_for_feedback_or_all'),
    url('^allgroupsoverview/(?P<assignmentid>\d+)/waiting_for_deliveries$',
        login_required(
            WaitingForDeliveriesOverview.as_view()),
        name='devilry_examiner_waiting_for_deliveries'),
    url('^allgroupsoverview/(?P<assignmentid>\d+)/corrected$',
        login_required(CorrectedOverview.as_view()),
        name='devilry_examiner_corrected'),
    url('^singlegroupoverview/(?P<groupid>\d+)$',
        login_required(SingleGroupOverview.as_view()),
        name='devilry_examiner_singlegroupoverview'),
    url('^singledelivery/(?P<deliveryid>\d+)$',
        login_required(SingleDeliveryView.as_view()),
        name='devilry_examiner_singledeliveryview'),
    url('^last_delivery_or_groupoverview/(?P<groupid>\d+)$',
        login_required(LastDeliveryOrGroupOverviewRedirectView.as_view()),
        name='devilry_examiner_last_delivery_or_groupoverview'),
    url('^add_deadline/(?P<assignmentid>\d+)$',
        login_required(AddDeadlineView.as_view()),
        name='devilry_examiner_add_deadline'),
    url('^close_groups/(?P<assignmentid>\d+)$',
        login_required(CloseGroupsView.as_view()),
        name='devilry_examiner_close_groups'),
    url('^add_nonelectronic_delivery/(?P<assignmentid>\d+)$',
        login_required(AddNonElectronicDeliveryView.as_view()),
        name='devilry_examiner_add_nonelectronic_delivery')
)


documentationregistry.add('devilry_examiner/gettingstarted', DevilryUserDocsProxy(
    en='examiner.html'))
