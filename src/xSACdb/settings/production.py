import socket

import dj_database_url

from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'xSACdb.mail.EnqueueBackend'
ALLOW_UNSAFE = os.environ.get('XSACDB_ALLOW_UNSAFE') == 'TRUE'

if ALLOW_UNSAFE:
    # Should be overriden by local_settings
    EMAIL_FROM = 'placeholder@xsacdb.wjdp.uk'
    ALLOWED_HOSTS = []
    CLUB = {'name': 'MadeUpSAC'}
    SECRET_KEY = 'abc123'
    GEOPOSITION_GOOGLE_MAPS_API_KEY = 'abc123'

try:
    from local_settings import *
except ImportError as e:
    if ALLOW_UNSAFE:
        print("local_settings.py is not present")
    else:
        raise e

# Some areas use this
DEFAULT_FROM_EMAIL = EMAIL_FROM

if 'RAVEN_CONFIG' in locals():
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.rq import RqIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    import xSACdb.version

    sentry_sdk.init(
        dsn=RAVEN_CONFIG['dsn'],
        integrations=[
            DjangoIntegration(),
            RqIntegration(),
            RedisIntegration(),
        ],
        release=xSACdb.version.RELEASE_SENTRY,
        environment='staging' if STAGING else 'production',
    )
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("site", CLUB['name'])
        scope.set_tag("version", xSACdb.version.VERSION)
else:
    RAVEN_CONFIG = {}

if 'XSACDB_CONTAINER' in os.environ and os.environ['XSACDB_CONTAINER'] == 'DOCKER':
    ALLOWED_HOSTS.append(socket.getaddrinfo(socket.gethostname(), b'http')[0][4][0])

    if 'DATABASE_URL' in os.environ:
        # If in a docker container, parse the database URL
        DATABASES = {
            'default': dj_database_url.parse(
                os.environ['DATABASE_URL']
            )
        }

        # Keep a database connection open. Kill at a defined limit to prevent leaks or other issues.
        # http://www.revsys.com/blog/2015/may/06/django-performance-simple-things/
        DATABASES['default']['CONN_MAX_AGE'] = 600

    if 'REDIS_URL' in os.environ:
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

# Webpack
WEBPACK_LOADER['DEFAULT']['CACHE'] = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
    },
    'formatters': {
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
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
        'rq.worker': {
            'handlers': ['rq_console'],
            'level': 'DEBUG'
        },
    }
}

# Password validation https://docs.djangoproject.com/en/2.2/topics/auth/passwords/#enabling-password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
