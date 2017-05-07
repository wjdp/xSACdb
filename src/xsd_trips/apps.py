from __future__ import unicode_literals

from django.apps import AppConfig


class TripsConfig(AppConfig):
    name = 'xsd_trips'
    verbose_name = 'Trips'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Trip'))
