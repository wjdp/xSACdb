from django.core.management.base import BaseCommand

from xSACdb.scheduler import init_scheduler


class Command(BaseCommand):
    help = 'Sets-up scheduled tasks. Should be called when application is deployed and after clearing the cache.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Setting up scheduled tasks...'))
        init_scheduler()
