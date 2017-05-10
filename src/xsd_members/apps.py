from __future__ import unicode_literals

from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'xsd_members'
    verbose_name = 'Members'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('MemberProfile'))
