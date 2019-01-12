from __future__ import absolute_import, unicode_literals

import socket
import dj_database_url
from raven.transport import RequestsHTTPTransport

from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'xSACdb.mail.EnqueueBackend'

from local_settings import *
from xSACdb.version import VERSION

# Patch debug apps into staging instances
# The production settings just mean production or production-like (running on Docker)
# Hence the possibility we could be running with DEBUG on.
if STAGING or DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + (
        'debug_toolbar',
        'django_extensions',
    )

    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

# Some areas use this
DEFAULT_FROM_EMAIL = EMAIL_FROM

if 'RAVEN_CONFIG' in locals():
    RAVEN_CONFIG['release'] = VERSION['tag']
    RAVEN_CONFIG['site'] = CLUB['name']
    # Async transport has issues with RQ http://python-rq.org/patterns/sentry/
    RAVEN_CONFIG['transport'] = RequestsHTTPTransport
else:
    RAVEN_CONFIG = {}

if 'XSACDB_CONTAINER' in os.environ and os.environ['XSACDB_CONTAINER'] == 'DOCKER':
    ALLOWED_HOSTS.append(socket.getaddrinfo(socket.gethostname(), b'http')[0][4][0])

    # If in a docker container, parse the database URL
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL']
        )
    }

    # Keep a database connection open. Kill at a defined limit to prevent leaks or other issues.
    # http://www.revsys.com/blog/2015/may/06/django-performance-simple-things/
    DATABASES['default']['CONN_MAX_AGE'] = 600

    # Cache data store
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': os.environ['REDIS_URL'],
            'KEY_PREFIX': os.environ['REDIS_KEY_PREFIX'],
        },
    }

    # Background task queues, uses same connection as django-redis-cache
    RQ_QUEUES = {
        'default': {
            'USE_REDIS_CACHE': 'default',
        },
    }

# Turn on cached loading of templates
TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Cache sessons (reads only, writes still go to database)
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Catch 404s
MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
) + MIDDLEWARE_CLASSES

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'rq_console': {
            'level': 'DEBUG',
            'class': 'rq.utils.ColorizingStreamHandler',
            'formatter': 'rq_console',
            'exclude': ['%(asctime)s'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'rq.worker': {
            'handlers': ['rq_console', 'sentry'],
            'level': 'DEBUG'
        },
    }
}
