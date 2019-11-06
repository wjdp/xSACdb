

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

# Define project paths
PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../../..')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
ASSETS_PATH = os.path.join(PROJECT_PATH, 'assets')
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
    r'^favicon.ico$',
    r'^manifest.json$',
    r'^inspect.json', # Uses an API key
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
    os.path.join(DIST_PATH, 'webpack'),
    ASSETS_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Caching for Django Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# HACK: WN doesn't seem to pick up dj compressor files as forever-cacheable
# TODO: Is this needed anymore?
WHITENOISE_MAX_AGE = 315360000

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': False, # set to true in production.py
        'BUNDLE_DIR_NAME': '/', # must end with slash
        'STATS_FILE': os.path.join(DIST_PATH, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': 20,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(CONF_PATH, 'templates'),
            os.path.join(SRC_PATH, 'templates_global'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'xSACdb.context_processors.xsd_vars',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'xSACdb.middleware.LoginRequiredMiddleware',
    'xSACdb.middleware.NewbieProfileFormRedirectMiddleware',
)

ROOT_URLCONF = 'xSACdb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'xSACdb.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

FIXTURE_DIRS = (
    os.path.join(SRC_PATH, 'xSACdb', 'fixtures'),
)

INSTALLED_APPS = (
    'redis_cache',  # https://github.com/sebleier/django-redis-cache
    'django_rq',  # https://github.com/ui/django-rq

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',

    'xsd_auth.apps.AuthConfig',
    'xsd_frontend.apps.FrontendConfig',
    'xsd_members.apps.MembersConfig',
    'xsd_training.apps.TrainingConfig',
    'xsd_trips.apps.TripsConfig',
    'xsd_sites.apps.SitesConfig',
    'xsd_kit',
    'xsd_about',
    'xsd_help',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'bootstrap3',
    'widget_tweaks',

    'geoposition',

    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare

    # Must be after apps creating activities
    'actstream',  # https://github.com/justquick/django-activity-stream

    'hijack',

    'compat',

    'health_check',
    # 'health_check_celery',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',

    'webpack_loader',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

AUTH_USER_MODEL = 'xsd_auth.User'
USER_MODEL = AUTH_USER_MODEL
AUTH_PROFILE_MODEL = 'xsd_members.MemberProfile'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_DISPLAY = 'xsd_auth.utils.get_user_display'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

# FIXME: Deprecated - use Django's AUTH_PASSWORD_VALIDATORS instead. (NEED DJ >=1.9)
ACCOUNT_PASSWORD_MIN_LENGTH = 8

SOCIALACCOUNT_FORMS = {
    'signup': 'xsd_auth.forms.SignupForm'
}

TEST_FIXTURES = [
    os.path.join(TMP_PATH, 'bsac_data.yaml'),
    'groups',
    'socialapp-test',
]

HIJACK_NOTIFY_USER = True
HIJACK_DISPLAY_ADMIN_BUTTON = False

ACTSTREAM_SETTINGS = {
    # 'MANAGER': 'myapp.managers.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_JSONFIELD': True,
}

PAGINATE_BY = 20

# Browser config
BROWSER_THEME_COLOUR = "#171f26"

# Inspect API
INSPECT_API_KEY_HASH = "033be85008caa4f26e04df5da463ee92218e4ff3bbf6565b4cee51abb0b0e973"
INSPECT_API_KEY_SALT = "EMQ2b6iDt96N"
