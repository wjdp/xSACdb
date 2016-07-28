"""All settings common to debug and production"""

import os
from sys import path

# Staging tag, when DEBUG is false and this true allows some unsafe behaviour.
STAGING = False
FAKER_LOCALE = 'en_GB'
RANDOM_SEED = 'The quick brown fox jumped over the lazy ocean diver'

# Make HTTPResponse do unicode
DEFAULT_CHARSET = 'utf-8'

ADMIN_MEDIA_PREFIX = ''

GOOGLE_MAPS_API_KEY = ''

# Define project paths
PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../../..')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
LIB_PATH = os.path.join(PROJECT_PATH, 'lib')
DIST_PATH = os.path.join(PROJECT_PATH, 'dist')
TMP_PATH = os.path.join(PROJECT_PATH, 'tmp')
CONF_PATH = os.path.join(PROJECT_PATH, 'conf')

# Add config dir to path
path.append(CONF_PATH)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

LOGIN_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
    # r'^media/', # allow any URL under /media/* This has facebook avatars, so NO!
    r'^static/',  # allow any URL under /static/*
    r'^facebook/',  # allow any URL under /facebook/*
    r'^accounts/',
    r'^hijack/',  # have their own protection
    r'^health/',  # Needs to be publicly accessible
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Media files (css, images etc) for development server
STATIC_DOC_ROOT = os.path.join(DIST_PATH, 'static')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIST_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CONF_PATH, 'static'),
    os.path.join(SRC_PATH, 'static_global'),
    LIB_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

# Caching for Django Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# django-compressor settings
# Curly braces doubled to escape them when using str.format()
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-sass', 'sass {{infile}} {{outfile}} --load-path {}'.format(LIB_PATH)),
    ('text/x-scss', 'sass --scss {{infile}} {{outfile}} --load-path {}'.format(LIB_PATH)),
)
# Lets the compress management command do it's work
COMPRESS_OFFLINE = True
# Prevents rebuilds if the source is unchanged
COMPRESS_CACHEABLE_PRECOMPILERS = (
    'text/coffeescript',
    'text/x-sass',
    'text/x-scss',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'xSACdb.middleware.LoginRequiredMiddleware',
    'xSACdb.middleware.NewbieProfileFormRedirectMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'xSACdb.context_processors.xsd_vars',
)

ROOT_URLCONF = 'xSACdb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'xSACdb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SRC_PATH, 'templates_global'),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'xSACdb.email_auth.EmailBackend',
)

FIXTURE_DIRS = (
    os.path.join(SRC_PATH, 'xSACdb', 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'xsd_auth',
    'xsd_frontend',
    'xsd_members',
    'xsd_training',
    'xsd_trips',
    'xsd_sites',
    'xsd_kit',
    'xsd_about',
    'xsd_help',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'bootstrap_toolkit',
    'bootstrap3',
    'compressor',
    'tastypie',
    'geoposition',
    'reversion',
    'django_rq',

    'debug_toolbar',
    'hijack',
    'compat',
    'raven.contrib.django.raven_compat',

    'health_check',
    # 'health_check_celery',
    'health_check_db',
    'health_check_cache',
    'health_check_storage',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_facebook.models': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

AUTH_USER_MODEL = 'xsd_auth.User'
USER_MODEL = AUTH_USER_MODEL
AUTH_PROFILE_MODEL = 'xsd_members.MemberProfile'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8

SOCIALACCOUNT_FORMS = {
    'signup': 'xsd_auth.forms.SignupForm'
}

SOCIALACCOUNT_ADAPTER = 'xsd_auth.adapter.XSDSocialAccountAdapter'

TEST_FIXTURES = [
    os.path.join(TMP_PATH, 'bsac_data.yaml'),
    'groups',
    'socialapp-test',
]

SILENCED_SYSTEM_CHECKS = ['1_6.W001']

HIJACK_NOTIFY_USER = True
HIJACK_DISPLAY_ADMIN_BUTTON = False

## Models to show in the activity stream

ACTIVITY_MODELS = [
    ('xsd_members', 'MemberProfile'),
    ('xsd_training', 'PerformedLesson'),
    ('xsd_training', 'PerformedSDC'),
    ('xsd_training', 'Session'),
    ('xsd_training', 'TraineeGroup'),
    ('xsd_sites', 'Site'),
]

## TODO HACK, disable email sending to prevent #173 on servers without email provision
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
