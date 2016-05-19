"""
WSGI config for xSACdb project.

Using combined Django and Whitenoise

"""
import os

# DJANGO_SETTINGS_MODULE must be set before doing anything
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xSACdb.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# Get the application object, then pass to whitenoise for union
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
