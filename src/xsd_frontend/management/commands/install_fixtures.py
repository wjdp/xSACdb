from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Install fixtures needed on a production instance.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Installing base fixtures...'))
        call_command('clear_cache')
        call_command('loaddata', 'groups')
        call_command('loaddata', 'membershiptypes')
        call_command('loaddata', 'tmp/bsac_data.yaml')
