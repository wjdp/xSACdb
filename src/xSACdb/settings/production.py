from __future__ import absolute_import
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

from .common import *
from local_settings import *

if 'XSACDB_CONTAINER' in os.environ and os.environ['XSACDB_CONTAINER'] == 'DOCKER':
    # If in a docker container, parse the database URL
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL']
        )
    }
