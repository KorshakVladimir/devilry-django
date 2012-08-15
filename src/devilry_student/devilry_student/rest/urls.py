from django.conf.urls.defaults import patterns, url

from .aggregated_groupinfo import AggregatedGroupInfo
from .add_delivery import AddDeliveryView
from .open_groups import OpenGroupsView
from .recent_deliveries import RecentDeliveriesView
from .recent_feedbacks import RecentFeedbacksView


urlpatterns = patterns('devilry_student.rest',
                       url(r'^aggregated-groupinfo/(?P<id>\d+)$', AggregatedGroupInfo.as_view()),
                       url(r'^add-delivery/(?P<id>\d+)$', AddDeliveryView.as_view()),
                       url(r'^open-groups/$', OpenGroupsView.as_view()),
                       url(r'^recent-deliveries/$', RecentDeliveriesView.as_view()),
                       url(r'^recent-feedbacks/$', RecentFeedbacksView.as_view())
                      )
