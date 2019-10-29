

from django.apps import AppConfig


class SitesConfig(AppConfig):
    name = 'xsd_sites'
    verbose_name = 'Dive Sites'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Site'))
