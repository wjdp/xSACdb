from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    # Taken from https://github.com/rdegges/django-clear-cache/blob/master/clear_cache/management/commands/clear_cache.py
    help = 'Fully clear your site-wide cache.'

    def handle(self, *args, **kwargs):
        try:
            assert settings.CACHES
            cache.clear()
            self.stdout.write('Your cache has been cleared!\n')
        except AttributeError:
            raise CommandError('You have no cache configured!\n')
