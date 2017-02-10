"""
WSGI config for xSACdb project.
"""
import os

# DJANGO_SETTINGS_MODULE must be set before doing anything
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xSACdb.settings")

from django.core.wsgi import get_wsgi_application

# Get the application object
application = get_wsgi_application()
