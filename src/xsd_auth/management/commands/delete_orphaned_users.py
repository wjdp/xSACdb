from django.core.management.base import BaseCommand

from xsd_auth.models import User


class Command(BaseCommand):
    help = 'Delete users without an attached member profile'

    def handle(self, *args, **options):
        qs = User.objects.filter(memberprofile=None)

        if qs.count() == 0:
            self.stdout.write('No orphaned users found in your database')
            return

        self.stdout.write('Found {} orphaned users:'.format(qs.count()))
        for u in qs:
            self.stdout.write('{}/{}/{}/{}'.format(u.username, u.email, u.first_name, u.last_name), ending='\n')

        self.stdout.write('\n Again that\'s {} orphaned users. Shall we delete them? [y/n]'.format(qs.count()))
        choice = raw_input().lower()

        if choice == 'y':
            qs.delete()
            self.stdout.write('Done')
        else:
            self.stdout.write('Abort')
