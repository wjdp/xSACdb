# Slightly faster testing on dev machines

from .development import *

# The default password hasher is rather slow by design. If you're authenticating many users in your tests, you may want
# to use a custom settings file and set the PASSWORD_HASHERS setting to a faster hashing algorithm:
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# WORKAROUND: https://code.djangoproject.com/ticket/24364 by reverting to default storage
from django.conf import global_settings
STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE
