# pylint: disable=wildcard-import,unused-wildcard-import

from pylab.settings.base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['pylab.lt', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pylab',
        'USER': 'pylab',
    }
}

LOGGING['root'] = {
    'level': 'WARNING',
    'handlers': ['stdout'],
}

SOCIALACCOUNT_PROVIDERS['persona']['AUDIENCE'] = 'pylab.lt'
