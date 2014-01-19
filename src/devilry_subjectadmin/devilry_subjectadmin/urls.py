from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.i18n import javascript_catalog
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from devilry_settings.i18n import get_javascript_catalog_packages
from .views import AppView
from .views import RedirectToSubjectAdminAppView
from .views import RedirectToGroupAdminAppView
from .exportdetailedperiodoverview import ExportDetailedPeriodOverview


@login_required
def emptyview(request):
    from django.http import HttpResponse
    return HttpResponse('Logged in')


i18n_packages = get_javascript_catalog_packages(
    'devilry_subjectadmin', 'devilry_extjsextras', 'devilry.apps.core')

urlpatterns = patterns(
    'devilry_subjectadmin',
    url('^rest/',
        include('devilry_subjectadmin.rest.urls')),
    url('^$', login_required(csrf_protect(ensure_csrf_cookie(AppView.as_view()))),
        name='devilry_subjectadmin'),
    # NOTE: Only used for testing
    url('^emptytestview', emptyview),
    url('^export/periodoverview/(?P<id>[^/]+)$',
        login_required(
            ExportDetailedPeriodOverview.as_view()),
        name='devilry_subjectadmin_export_period_details'),
    url('^i18n.js$', javascript_catalog, kwargs={'packages': i18n_packages},
        name='devilry_subjectadmin_i18n'),

    # Views that just redirect to ``/devilry_subjectadmin/#<some-path>``
    url('^subject/(?P<id>[^/]+)',
        login_required(RedirectToSubjectAdminAppView.as_view(pathformat='/subject/{id}/')),
        name='devilry_subjectadmin_subject'),

    # Views that just redirect to ``/devilry_subjectadmin/#<some-path>``
    url('^subject/(?P<id>\d+)',
        login_required(RedirectToSubjectAdminAppView.as_view(pathformat='/subject/{id}/')),
        name='devilry_subjectadmin_subject'),
    url('^period/(?P<id>\d+)',
        login_required(RedirectToSubjectAdminAppView.as_view(pathformat='/period/{id}/')),
        name='devilry_subjectadmin_period'),
    url('^assignment/(?P<id>\d+)',
        login_required(RedirectToSubjectAdminAppView.as_view(pathformat='/assignment/{id}/')),
        name='devilry_subjectadmin_assignment'),
    url('^group/(?P<id>\d+)',
        login_required(RedirectToGroupAdminAppView.as_view()),
        name='devilry_subjectadmin_group'),
)