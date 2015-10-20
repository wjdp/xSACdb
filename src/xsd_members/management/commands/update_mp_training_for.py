from django.core.management.base import BaseCommand, CommandError
from xsd_members.models import MemberProfile

class Command(BaseCommand):
    help = 'Updates all training_for cached values'

    def handle(self, *args, **options):
        mps = MemberProfile.objects.all()
        for mp in mps:
            mp.update_training_for()
            print "{}: {}".format(mp, mp.training_for)
            mp.save()
