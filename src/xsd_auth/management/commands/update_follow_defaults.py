from django.core.management.base import BaseCommand

from xsd_auth.models import User


class Command(BaseCommand):
    help = 'Update user\'s default follows'

    def handle(self, *args, **options):
        for user in User.objects.all():
            user.follow_defaults()
