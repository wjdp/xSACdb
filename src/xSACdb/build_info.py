from __future__ import unicode_literals

import datetime
import os

from django.conf import settings

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
