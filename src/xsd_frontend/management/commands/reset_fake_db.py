from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Wipe database and install fixtures and fake data.'

    def handle(self, *args, **kwargs):
        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You may only run this command in DEBUG or STAGING')

        self.stdout.write(self.style.MIGRATE_HEADING('Flushing database and reinstalling fake data...'))

        # Clear everything out
        call_command('flush', '--noinput')

        # Prod fixtures
        call_command('loaddata', 'groups')
        call_command('loaddata', 'membershiptypes')
        call_command('loaddata', 'tmp/bsac_data.yaml')
        # Static fake data
        call_command('loaddata', 'example_sites')
        # Dynamic fake data
        call_command('generate_fake_data')
        # reversion
        call_command('createinitialrevisions')
