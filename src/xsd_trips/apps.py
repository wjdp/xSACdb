from __future__ import unicode_literals

from django.apps import AppConfig
from actstream import registry


class TripsConfig(AppConfig):
    name = 'xsd_trips'
    verbose_name = 'Trips'

    def ready(self):
        registry.register(self.get_model('Trip'))
