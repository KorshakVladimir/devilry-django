from .base import *

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_EAGER_TRANSACTION = True
BROKER_BACKEND = 'memory'

if 'devilry.utils.logexceptionsmiddleware.TracebackLoggingMiddleware' in MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES.remove('devilry.utils.logexceptionsmiddleware.TracebackLoggingMiddleware')

# Use database for search in tests
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Ensures we are testing against the default translation strings.
DEVILRY_JAVASCRIPT_LOCALE_OVERRIDE_APPS = []

# Default to skipping selenium tests
SKIP_SELENIUMTESTS = True
# SELENIUM_BROWSER = 'phantomjs'
# SELENIUM_DEFAULT_TIMEOUT = 20


# Disable migrations when running tests
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
