# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# noinspection PyUnresolvedReferences
from .common import *

ALLOWED_HOSTS = ['*']

# Club config
CLUB = {
    # Name of your club
    'name': 'MadeUpSAC',

    # Are you a student club? This adds fields like student ID to the member records
    'student': True,

    'how_to_renew': 'Renew at <a href="http://su.nottingham.ac.uk/sub-aqua">http://su.nottingham.ac.uk/sub-aqua</a>',
    'bsac_club_renew': 'Contact the VP for details.',
}

# Send error reports to
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Your database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xsacdb',  # Or path to database file if using sqlite3.
        'USER': 'runner',  # Not used with sqlite3.
        'PASSWORD': 'runner-password',  # Not used with sqlite3.
        'HOST': 'postgres',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Cache data store
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis:6379',
    },
}

# Background task queues, uses same connection as django-redis-cache
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'redis-cache',
    },
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

# The default password hasher is rather slow by design. If you're authenticating many users in your tests, you may want
# to use a custom settings file and set the PASSWORD_HASHERS setting to a faster hashing algorithm:
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# django-geoposition dummy API key
GEOPOSITION_GOOGLE_MAPS_API_KEY = 'dummy'
