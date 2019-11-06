import datetime
import os

from django.conf import settings

from xSACdb import version

PRE_FILE = os.path.join(settings.DIST_PATH, 'pre.timestamp')
POST_FILE = os.path.join(settings.DIST_PATH, 'post.timestamp')
DEPLOY_FILE = os.path.join(settings.DIST_PATH, 'deploy.timestamp')


def get_time(filename):
    """Given a filename of a file containing a unix timestamp return a datetime"""
    try:
        with open(filename, 'r') as f:
            return datetime.datetime.fromtimestamp(int(f.read()))
    except IOError:
        return None


def get_environment_name():
    if settings.DEBUG:
        return 'development'
    elif settings.STAGING:
        return 'staging'
    else:
        return 'production'


def get_version():
    return version.VERSION['tag']
