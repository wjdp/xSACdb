from django.core.management.base import BaseCommand
from django.template.loader import get_template

from xsd_frontend.activity import XSDAction


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    # Taken from https://github.com/rdegges/django-clear-cache/blob/master/clear_cache/management/commands/clear_cache.py
    help = 'Builds the cache of version diffs.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('Building version cache...'))
        diff_template = get_template('versioning/diff.html')
        i = 1
        for action in XSDAction.objects.all():
            if len(action.versions) == 0:
                continue
            for version in action.versions:
                if i % 10 == 0:
                    self.stdout.write("{} ".format(version.pk), ending="\n")
                else:
                    self.stdout.write("{} ".format(version.pk), ending="")
                i += 1
                diff_template.render({
                    'version': version,
                })
        self.stdout.write("Done")
