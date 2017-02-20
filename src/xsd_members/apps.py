from __future__ import unicode_literals

from django.apps import AppConfig
from actstream import registry


class MembersConfig(AppConfig):
    name = 'xsd_members'
    verbose_name = 'Members'

    def ready(self):
        registry.register(self.get_model('MemberProfile'))
