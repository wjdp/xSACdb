from django.core.management.base import BaseCommand, CommandError
from django.db import connection

class Command(BaseCommand):
    help = 'Updates all MP cached values'

    def handle(self, *args, **options):
        print 'Running nu-6 to nu-7 user migrations'
        cursor = connection.cursor()
        print cursor.execute('INSERT INTO xsd_auth_user SELECT * FROM auth_user;')
        print cursor.execute('INSERT INTO xsd_auth_user_groups SELECT * FROM auth_user_groups;')
        print cursor.execute('DROP TABLE auth_user;')
        print cursor.execute('DROP TABLE auth_user_groups;')
        print 'Done'
