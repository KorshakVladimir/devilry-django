from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import patterns, url

from .views import EmailSendingDebug

urlpatterns = patterns('devilry.apps.send_email_to_students',
                       url(r'^email_sending_debug/(?P<username>\w+)$',
                           login_required(EmailSendingDebug.as_view()),
                           name='send_email_to_students_email_sending_debug')
                      )
