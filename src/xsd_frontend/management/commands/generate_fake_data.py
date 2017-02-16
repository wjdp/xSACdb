from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from xSACdb.roles.groups import *

from xsd_training.models import *

from faker import Factory
import random

class Command(BaseCommand):
    help = 'Generates fake data for testing, demo site and development'
    fake = None
    FLUFFY_USER_COUNT = 99

    def setUp(self):
        self.OD = Qualification.objects.get(code="OD")
        self.SD = Qualification.objects.get(code="SD")
        self.DL = Qualification.objects.get(code="DL")
        self.AD = Qualification.objects.get(code="AD")
        self.FC = Qualification.objects.get(code="FC")

        self.PERSONAL_QUALS = [self.OD, self.SD, self.DL, self.AD, self.FC]

        self.ADI = Qualification.objects.get(code="ADI")
        self.PI = Qualification.objects.get(code="PI")
        self.THI = Qualification.objects.get(code="THI")
        self.AOWI = Qualification.objects.get(code="AOWI")
        self.OWI = Qualification.objects.get(code="OWI")
        self.AI = Qualification.objects.get(code="AI")
        self.NI = Qualification.objects.get(code="NI")

        self.INSTRUCTOR_QUALS = [self.ADI, self.PI, self.THI, self.AOWI, self.OWI,
                                 self.AI, self.NI]

        self.OO1 = Lesson.objects.get(code="OO1")
        self.OO2 = Lesson.objects.get(code="OO2")
        self.SO1 = Lesson.objects.get(code="SO1")

        self.BOAT_HANDLING = SDC.objects.get(title="Boat Handling")
        self.WRECK_APPRECIATION = SDC.objects.get(title="Wreck Appreciation")

    def handle(self, *args, **options):
        from django.conf import settings

        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        self.setUp()

        self.fake = Factory.create(settings.FAKER_LOCALE)
        # Manually force seed, otherwise it's done by time, which could lead to inconsistent tests
        self.fake.seed(settings.RANDOM_SEED)
        random.seed(settings.RANDOM_SEED)

        with transaction.atomic():
            self.stdout.write('Generating fake data...')
            self.generateUsefulUsers()
            self.generateFluffyUsers()
            self.stdout.write('Done')

    def generateUsefulUsers(self):
        U = get_user_model()

        groupAdmin = Group.objects.get(pk=GROUP_ADMIN)
        groupTraining = Group.objects.get(pk=GROUP_TRAINING)
        groupTrips = Group.objects.get(pk=GROUP_TRIPS)
        groupSites = Group.objects.get(pk=GROUP_SITES)
        groupMembers = Group.objects.get(pk=GROUP_MEMBERS)
        groupDO = Group.objects.get(pk=GROUP_DO)

        superUser = U.objects.create_user(
            email="superuser@xsacdb.wjdp.uk",
            password="su",
            first_name="SUPER",
            last_name="USER",
        )
        superUser.username = "su"
        superUser.is_superuser = True
        superUser.is_staff = True
        superUser.save()
        superUser.groups.add(groupAdmin)
        superUser.save()
        superUser.memberprofile.approve()
        superUser.memberprofile.fake(self.fake)
        superUser.memberprofile.save()

        divingOfficer = U.objects.create_user(
            email="do@xsacdb.wjdp.uk",
            password="do",
            first_name=self.fake.first_name(),
            last_name="Divingofficer",
        )
        divingOfficer.username = "do"
        divingOfficer.save()
        divingOfficer.groups.add(groupDO)
        divingOfficer.save()
        divingOfficer.memberprofile.approve()
        divingOfficer.memberprofile.fake(self.fake)
        divingOfficer.memberprofile.set_qualification(self.AD)
        divingOfficer.memberprofile.set_qualification(self.OWI)
        divingOfficer.memberprofile.save()

        trainingOfficer = U.objects.create_user(
            email="to@xsacdb.wjdp.uk",
            password="to",
            first_name=self.fake.first_name(),
            last_name="Trainingofficer",
        )
        trainingOfficer.username = "to"
        trainingOfficer.save()
        trainingOfficer.groups.add(groupTraining)
        trainingOfficer.save()
        trainingOfficer.memberprofile.approve()
        trainingOfficer.memberprofile.fake(self.fake)
        trainingOfficer.memberprofile.set_qualification(self.DL)
        trainingOfficer.memberprofile.set_qualification(self.OWI)
        trainingOfficer.memberprofile.save()

        membersOfficer = U.objects.create_user(
            email="mo@xsacdb.wjdp.uk",
            password="mo",
            first_name=self.fake.first_name(),
            last_name="Membersofficer",
        )
        membersOfficer.username = "mo"
        membersOfficer.save()
        membersOfficer.groups.add(groupMembers)
        membersOfficer.save()
        membersOfficer.memberprofile.approve()
        membersOfficer.memberprofile.fake(self.fake)
        membersOfficer.memberprofile.set_qualification(self.SD)
        membersOfficer.memberprofile.set_qualification(self.THI)
        membersOfficer.memberprofile.save()

        od1 = U.objects.create_user(
            email="od1@xsacdb.wjdp.uk",
            password="od1",
            first_name=self.fake.first_name(),
            last_name="Oceandiver",
        )
        od1.username = "od1"
        od1.save()
        od1.memberprofile.approve()
        od1.memberprofile.fake(self.fake)
        od1.memberprofile.set_qualification(self.OD)
        od1.memberprofile.save()

        od2 = U.objects.create_user(
            email="od2@xsacdb.wjdp.uk",
            password="od2",
            first_name=self.fake.first_name(),
            last_name="Oceandiver",
        )
        od2.username = "od2"
        od2.save()
        od2.memberprofile.approve()
        od2.memberprofile.fake(self.fake)
        od2.memberprofile.set_qualification(self.OD)
        od2.memberprofile.save()

        sd1 = U.objects.create_user(
            email="sd1@xsacdb.wjdp.uk",
            password="sd1",
            first_name=self.fake.first_name(),
            last_name="Sportsdiver",
        )
        sd1.username = "sd1"
        sd1.save()
        sd1.memberprofile.approve()
        sd1.memberprofile.fake(self.fake)
        sd1.memberprofile.set_qualification(self.SD)
        sd1.memberprofile.save()

        sd2 = U.objects.create_user(
            email="sd2@xsacdb.wjdp.uk",
            password="sd2",
            first_name=self.fake.first_name(),
            last_name="Sportsdiver",
        )
        sd2.username = "sd2"
        sd2.save()
        sd2.memberprofile.approve()
        sd2.memberprofile.fake(self.fake)
        sd2.memberprofile.set_qualification(self.SD)
        sd2.memberprofile.save()

        dl1 = U.objects.create_user(
            email="dl1@xsacdb.wjdp.uk",
            password="dl1",
            first_name=self.fake.first_name(),
            last_name="Diveleader",
        )
        dl1.username = "dl1"
        dl1.save()
        dl1.memberprofile.approve()
        dl1.memberprofile.fake(self.fake)
        dl1.memberprofile.set_qualification(self.DL)
        dl1.memberprofile.save()

        owi1 = U.objects.create_user(
            email="owi@xsacdb.wjdp.uk",
            password="owi1",
            first_name=self.fake.first_name(),
            last_name="Openwaterinstructor",
        )
        owi1.username = "owi1"
        owi1.save()
        owi1.memberprofile.approve()
        owi1.memberprofile.fake(self.fake)
        owi1.memberprofile.set_qualification(self.DL)
        owi1.memberprofile.set_qualification(self.OWI)
        owi1.memberprofile.save()

    def generateFluffyUsers(self):
        U = get_user_model()

        for i in range(0, self.FLUFFY_USER_COUNT):
            u = U.objects.create_user(
                email = self.fake.email(),
                password = "guest",
                first_name = self.fake.first_name(),
                last_name=self.fake.last_name(),
            )
            u.save()
            if self.fake.boolean(chance_of_getting_true=90):
                u.memberprofile.fake(self.fake)
                if self.fake.boolean(chance_of_getting_true=80):
                    u.memberprofile.approve()
                if self.fake.boolean(chance_of_getting_true=90):
                    u.memberprofile.set_qualification(random.choice(self.PERSONAL_QUALS))
                    if self.fake.boolean(chance_of_getting_true=10):
                        u.memberprofile.set_qualification(random.choice(self.INSTRUCTOR_QUALS))
                        # if u.memberprofile.top_instructor_qual().rank >= self.OWI.rank:
                        #     u.memberprofile.instructor_number = random.randrange(1234,99999)
            if self.fake.boolean(chance_of_getting_true=2):
                # Archive some
                u.memberprofile.archive()
            u.memberprofile.save()
