from __future__ import absolute_import
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

from .common import *
from local_settings import *
from xSACdb.version import VERSION

if 'RAVEN_CONFIG' in locals():
    RAVEN_CONFIG['release'] = VERSION['tag']
    RAVEN_CONFIG['site'] = CLUB['name']
else:
    RAVEN_CONFIG = {}

if 'XSACDB_CONTAINER' in os.environ and os.environ['XSACDB_CONTAINER'] == 'DOCKER':
    # If in a docker container, parse the database URL
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL']
        )
    }

    # Cache data store
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': os.environ['REDIS_URL'],
        },
    }

    # Background task queues, uses same connection as django-redis-cache
    RQ_QUEUES = {
        'default': {
            'USE_REDIS_CACHE': 'default',
        },
    }
