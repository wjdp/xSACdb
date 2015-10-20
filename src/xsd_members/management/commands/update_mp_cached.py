from django.core.management.base import BaseCommand, CommandError
from xsd_members.models import MemberProfile

class Command(BaseCommand):
    help = 'Updates all MP cached values'

    def handle(self, *args, **options):
        mps = MemberProfile.objects.all()
        for mp in mps:
            mp.save()
