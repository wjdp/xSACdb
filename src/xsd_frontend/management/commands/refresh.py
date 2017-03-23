from django.core.management.base import BaseCommand

from django.core.management import call_command


class Command(BaseCommand):
    help = 'Clears and refills ephemeral things, like the cache.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_LABEL('Refreshing ephemeral stores...'))
        call_command('clear_cache')
        call_command('setup_scheduler')
        call_command('build_version_cache')
        self.stdout.write(self.style.MIGRATE_SUCCESS('All done :)'))
