from django.core.management.base import BaseCommand

from xSACdb.scheduler import init_scheduler


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    # Taken from https://github.com/rdegges/django-clear-cache/blob/master/clear_cache/management/commands/clear_cache.py
    help = 'Fully clear your site-wide cache.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Setting up scheduled tasks...'))
        init_scheduler()
