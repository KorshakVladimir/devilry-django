from setuptools import setup, find_packages

setup(
    name = "devilry",
    version = "1.3-beta1",
    url = 'http://devilry.org',
    license = 'BSD',
    description = "A system for handling electronic deliveries.",
    author = 'The Devilry developers',
    packages = find_packages(),
    install_requires = ['setuptools', 'Django', 'Markdown', 'django_errortemplates',
                        'djangorestframework', 'Pygments',
                        'django-haystack',
                        'pysolr',
                        'httplib2',
                        #'flup',
                        #'PyYAML',
                        'django-celery',
                        'devilry_rest', # NOTE: We only need this until all modules importing from ``devilry.utils.rest*`` is updated
                        'gunicorn']
)
