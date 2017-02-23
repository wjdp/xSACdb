from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send email confirmations for unverified primary email addresses.'

    # Needed because we did our own register view, didn't go through allauth

    def handle(self, *args, **options):
        for addr in EmailAddress.objects.filter(verified=False):
            if not addr.user.profile.archived:
                addr.send_confirmation()
