from __future__ import unicode_literals

from django.apps import AppConfig
from actstream import registry


class SitesConfig(AppConfig):
    name = 'xsd_sites'
    verbose_name = 'Dive Sites'

    def ready(self):
        registry.register(self.get_model('Site'))
