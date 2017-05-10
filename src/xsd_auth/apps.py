from __future__ import unicode_literals

from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'xsd_auth'
    verbose_name = 'Auth'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('User'))
