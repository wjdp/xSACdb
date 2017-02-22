from allauth.account.utils import sync_user_email_addresses
from django.core.management.base import BaseCommand

from xsd_auth.models import User


class Command(BaseCommand):
    help = 'Ensure an EmailAddress exists for all users.'

    # Needed because we did our own register view, didn't go through allauth

    def handle(self, *args, **options):
        for user in User.objects.all():
            sync_user_email_addresses(user)
