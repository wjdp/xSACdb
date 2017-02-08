from __future__ import absolute_import
import os

# Make this FALSE for deployment
DEBUG = True
TEMPLATE_DEBUG = True

from .common import *

# Club config
CLUB = {
    # Name of your club
    'name': 'MadeUpSAC',

    # Are you a student club? This adds fields like student ID to the member records
    'student': True,

    'how_to_renew': 'Renew at <a href="http://su.nottingham.ac.uk/sub-aqua">su.nottingham.ac.uk/sub-aqua</a>.',
    'bsac_club_renew': 'Contact the VP for details.',
    'medical_form_renew': 'Form available at <a href="http://uksdmc.co.uk/">uksdmc.co.uk</a>.',
}

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

# Send error reports to
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Your database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(TMP_PATH, 'db.sqlite3'),  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

# Make this unique, and don't share it with anybody.
# Generate one here: http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'change me!'

RAVEN_CONFIG = {}

# Test css and js compression, True in prod
# COMPRESS_ENABLED = True

# Background task queues
# RQ_QUEUES = {
#     'default': {
#         'HOST': 'localhost',
#         'PORT': 6379,
#         'DB': 0,
#         'PASSWORD': '',
#         'DEFAULT_TIMEOUT': 360,
#     },
#     # 'high': {
#     #     'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
#     #     'DEFAULT_TIMEOUT': 500,
#     # },
#     # 'low': {
#     #     'HOST': 'localhost',
#     #     'PORT': 6379,
#     #     'DB': 0,
#     # }
# }

# Cache data store
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

# Background task queues, uses same connection as django-redis-cache
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'tmp/emails/' # change this to a proper location
