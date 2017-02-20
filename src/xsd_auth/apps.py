from __future__ import unicode_literals

from django.apps import AppConfig
from actstream import registry


class AuthConfig(AppConfig):
    name = 'xsd_auth'
    verbose_name = 'Auth'

    def ready(self):
        registry.register(self.get_model('User'))
