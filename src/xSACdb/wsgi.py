"""
WSGI config for xSACdb project.
"""
import os
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# DJANGO_SETTINGS_MODULE must be set before doing anything
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xSACdb.settings")

from django.core.wsgi import get_wsgi_application

# Get the application object
application = Sentry(get_wsgi_application())
