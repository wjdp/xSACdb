from __future__ import unicode_literals

import random

from allauth.account.models import EmailAddress
from allauth.account.utils import sync_user_email_addresses
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from faker import Factory

from xSACdb.roles.groups import *
from xsd_members.models import MemberProfile
from xsd_sites.models import Site
from xsd_training.models import *
from xsd_trips.models import Trip
from xsd_trips.models.trip_member import TripMember
from xsd_trips.models.trip_state import STATE_OPEN, STATE_CLOSED, STATE_COMPLETED, STATE_CANCELLED


class Command(BaseCommand):
    help = 'Generates fake data for testing, demo site and development'
    fake = None
    FLUFFY_USER_COUNT = 150
    TG_COUNT = 15
    TG_MAX_SIZE = 25
    SS_COUNT = 50
    PL_COUNT = 500
    PSDC_COUNT = 50
    TRIP_COUNT = 300

    def setUp(self):
        self.OD = Qualification.objects.get(code="OD")
        self.SD = Qualification.objects.get(code="SD")
        self.DL = Qualification.objects.get(code="DL")
        self.AD = Qualification.objects.get(code="AD")
        self.FC = Qualification.objects.get(code="FC")

        self.PERSONAL_QUALS = [self.OD, self.SD, self.DL, self.AD, self.FC]

        self.ADI = Qualification.objects.get(code="ADI")
        self.PI = Qualification.objects.get(code="PI")
        self.TI = Qualification.objects.get(code="TI")
        self.AOWI = Qualification.objects.get(code="AOWI")
        self.OWI = Qualification.objects.get(code="OWI")
        self.AI = Qualification.objects.get(code="AI")
        self.NI = Qualification.objects.get(code="NI")

        self.INSTRUCTOR_QUALS = [self.ADI, self.PI, self.TI, self.AOWI, self.OWI,
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

            # Members
            self.generateUsefulUsers()
            self.generateFluffyUsers()

            # Training
            self.generateTrainingGroups()
            self.generateSessions()
            self.generatePerformedLessons()

            # Trips
            self.generateTrips()
            self.fillTrips()

            self.stdout.write('Done')

    def status_write(self, message):
        self.stdout.write('  {}'.format(message))

    def verifyEmail(self, user):
        sync_user_email_addresses(user)
        ea = EmailAddress.objects.get_for_user(user, user.email)
        ea.verified = True
        ea.save()

    def generateUsefulUsers(self):
        U = get_user_model()

        groupAdmin = Group.objects.get(pk=GROUP_ADMIN)
        groupTraining = Group.objects.get(pk=GROUP_TRAINING)
        groupTrips = Group.objects.get(pk=GROUP_TRIPS)
        groupSites = Group.objects.get(pk=GROUP_SITES)
        groupMembers = Group.objects.get(pk=GROUP_MEMBERS)
        groupDO = Group.objects.get(pk=GROUP_DO)

        superUser = U.objects.create_superuser(
            username="su",
            email="superuser@xsacdb.wjdp.uk",
            password="su",
            first_name="SUPER",
            last_name="USER",
        )
        superUser.save()
        superUser.groups.add(groupAdmin)
        superUser.save()
        superUser.memberprofile.fake(self.fake)
        superUser.memberprofile.save()
        self.verifyEmail(superUser)

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
        divingOfficer.memberprofile.approve(superUser)
        divingOfficer.memberprofile.fake(self.fake)
        divingOfficer.memberprofile.set_qualification(self.AD)
        divingOfficer.memberprofile.set_qualification(self.OWI)
        divingOfficer.memberprofile.save()
        self.verifyEmail(divingOfficer)

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
        trainingOfficer.memberprofile.approve(superUser)
        trainingOfficer.memberprofile.fake(self.fake)
        trainingOfficer.memberprofile.set_qualification(self.DL)
        trainingOfficer.memberprofile.set_qualification(self.OWI)
        trainingOfficer.memberprofile.save()
        self.verifyEmail(trainingOfficer)

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
        membersOfficer.memberprofile.approve(superUser)
        membersOfficer.memberprofile.fake(self.fake)
        membersOfficer.memberprofile.set_qualification(self.SD)
        membersOfficer.memberprofile.set_qualification(self.TI)
        membersOfficer.memberprofile.save()
        self.verifyEmail(membersOfficer)

        od1 = U.objects.create_user(
            email="od1@xsacdb.wjdp.uk",
            password="od1",
            first_name=self.fake.first_name(),
            last_name="Oceandiver",
        )
        od1.username = "od1"
        od1.save()
        od1.memberprofile.approve(membersOfficer)
        od1.memberprofile.fake(self.fake)
        od1.memberprofile.set_qualification(self.OD)
        od1.memberprofile.save()
        self.verifyEmail(od1)

        od2 = U.objects.create_user(
            email="od2@xsacdb.wjdp.uk",
            password="od2",
            first_name=self.fake.first_name(),
            last_name="Oceandiver",
        )
        od2.username = "od2"
        od2.save()
        od2.memberprofile.approve(membersOfficer)
        od2.memberprofile.fake(self.fake)
        od2.memberprofile.set_qualification(self.OD)
        od2.memberprofile.save()
        self.verifyEmail(od2)

        sd1 = U.objects.create_user(
            email="sd1@xsacdb.wjdp.uk",
            password="sd1",
            first_name=self.fake.first_name(),
            last_name="Sportsdiver",
        )
        sd1.username = "sd1"
        sd1.save()
        sd1.memberprofile.approve(membersOfficer)
        sd1.memberprofile.fake(self.fake)
        sd1.memberprofile.set_qualification(self.SD)
        sd1.memberprofile.save()
        self.verifyEmail(sd1)

        sd2 = U.objects.create_user(
            email="sd2@xsacdb.wjdp.uk",
            password="sd2",
            first_name=self.fake.first_name(),
            last_name="Sportsdiver",
        )
        sd2.username = "sd2"
        sd2.save()
        sd2.memberprofile.approve(membersOfficer)
        sd2.memberprofile.fake(self.fake)
        sd2.memberprofile.set_qualification(self.SD)
        sd2.memberprofile.save()
        self.verifyEmail(sd2)

        dl1 = U.objects.create_user(
            email="dl1@xsacdb.wjdp.uk",
            password="dl1",
            first_name=self.fake.first_name(),
            last_name="Diveleader",
        )
        dl1.username = "dl1"
        dl1.save()
        dl1.memberprofile.approve(membersOfficer)
        dl1.memberprofile.fake(self.fake)
        dl1.memberprofile.set_qualification(self.DL)
        dl1.memberprofile.save()
        self.verifyEmail(dl1)

        dl2 = U.objects.create_user(
            email="dl2@xsacdb.wjdp.uk",
            password="dl2",
            first_name=self.fake.first_name(),
            last_name="Diveleader",
        )
        dl2.username = "dl2"
        dl2.save()
        dl2.memberprofile.approve(membersOfficer)
        dl2.memberprofile.fake(self.fake)
        dl2.memberprofile.set_qualification(self.DL)
        dl2.memberprofile.save()
        self.verifyEmail(dl2)

        owi1 = U.objects.create_user(
            email="owi@xsacdb.wjdp.uk",
            password="owi1",
            first_name=self.fake.first_name(),
            last_name="Openwaterinstructor",
        )
        owi1.username = "owi1"
        owi1.save()
        owi1.memberprofile.approve(membersOfficer)
        owi1.memberprofile.fake(self.fake)
        owi1.memberprofile.set_qualification(self.DL)
        owi1.memberprofile.set_qualification(self.OWI)
        owi1.memberprofile.save()
        self.verifyEmail(owi1)

        self.usefulUsers = {
            'su': superUser,
            'do': divingOfficer,
            'to': trainingOfficer,
            'mo': membersOfficer,
            'od1': od1,
            'od2': od2,
            'sd1': sd1,
            'sd2': sd2,
            'dl1': dl1,
            'dl2': dl2,
            'owi1': owi1,
        }

        self.usefulUsersArray = [
            superUser,
            divingOfficer,
            trainingOfficer,
            membersOfficer,
            od1, od2,
            sd1, sd2,
            dl1, dl2,
            owi1,
        ]

        self.memberActionUsers = [
            superUser,
            divingOfficer,
            membersOfficer
        ]

        self.status_write('Generated useful users')

    def generateFluffyUsers(self):
        U = get_user_model()

        for i in range(0, self.FLUFFY_USER_COUNT):
            u = U.objects.create_user(
                email=self.fake.email(),
                password="guest",
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
            )
            u.save()
            if self.fake.boolean(chance_of_getting_true=90):
                u.memberprofile.fake(self.fake)
                if self.fake.boolean(chance_of_getting_true=80):
                    self.verifyEmail(u)
                else:
                    sync_user_email_addresses(u)
                if self.fake.boolean(chance_of_getting_true=80):
                    u.memberprofile.approve(random.choice(self.memberActionUsers))
                if self.fake.boolean(chance_of_getting_true=90):
                    u.memberprofile.set_qualification(random.choice(self.PERSONAL_QUALS))
                    if self.fake.boolean(chance_of_getting_true=10):
                        u.memberprofile.set_qualification(random.choice(self.INSTRUCTOR_QUALS))
                        # if u.memberprofile.top_instructor_qual().rank >= self.OWI.rank:
                        #     u.memberprofile.instructor_number = random.randrange(1234,99999)
            if self.fake.boolean(chance_of_getting_true=10):
                # Archive some
                u.memberprofile.archive(random.choice(self.memberActionUsers))
            u.memberprofile.save()

        self.status_write('Generated {} fluffy users'.format(self.FLUFFY_USER_COUNT))

    def generateTrainingGroups(self):
        def fill_group(group, qual, count):
            # Group will contain no more than count trainees. It may contain less.
            ts = []
            for i in range(0, count):
                t = random.choice(MemberProfile.objects.filter(top_qual_cached=qual))
                if t not in ts:
                    ts.append(t)
                    group.trainees.add(t)
            group.save()

        y = datetime.date.today().year
        self.tg_od1 = TraineeGroup.objects.create(name="Ocean Diver {}".format(y))
        self.tg_od1.trainees.add(self.usefulUsers['su'].profile) # SU should be an ocean diver
        fill_group(self.tg_od1, None, random.randint(8,self.TG_MAX_SIZE))
        self.tg_od2 = TraineeGroup.objects.create(name="Ocean Diver {}".format(y-1))
        fill_group(self.tg_od2, None, random.randint(8,self.TG_MAX_SIZE))
        self.tg_sd1 = TraineeGroup.objects.create(name="Sports Diver {}".format(y))
        fill_group(self.tg_sd1, self.OD, random.randint(8,self.TG_MAX_SIZE))
        self.tg_sd2 = TraineeGroup.objects.create(name="Sports Diver {}".format(y-1))
        fill_group(self.tg_sd2, self.OD, random.randint(8,self.TG_MAX_SIZE))
        self.tg_dl1 = TraineeGroup.objects.create(name="Dive Leader {}".format(y))
        fill_group(self.tg_dl1, self.SD, random.randint(8,self.TG_MAX_SIZE))

        self.status_write('Generated useful training groups')

        for i in range(0, self.TG_COUNT):
            g = TraineeGroup.objects.create(name=' '.join(self.fake.words(nb=random.randint(2,4))))
            fill_group(g, random.choice([None, self.OD, self.SD, self.DL, self.AD, self.FC]), random.randint(1,15))

        self.status_write('Generated {} fluffy training groups'.format(self.TG_COUNT))

    def generateSessions(self):
        instructors = MemberProfile.objects.filter(is_instructor_cached=True)
        sites = Site.objects.filter(type='TR')

        def session_name(mode, qual):
            if mode=='AS':
                return "{} Theory Exam".format(qual.title)
            else:
                return "{}{}".format(self.fake.word(), random.randint(0, 9)),

        for i in range(0, self.SS_COUNT):
            mode = random.choice(['TH', 'SW', 'OW', 'AS'])
            g = random.choice([
                (self.tg_od1, self.OD),
                (self.tg_od2, self.OD),
                (self.tg_sd1, self.SD),
                (self.tg_sd2, self.SD),
                # (self.tg_dl1, self.DL),
            ])
            s = Session.objects.create(
                name = session_name(mode, g[1]),
                when = self.fake.date_time_between(start_date="-3y", end_date="+120d"),
                where = random.choice(sites),
                notes = '\n\n'.join(self.fake.paragraphs(nb=random.randint(0,3)))
            )
            ts = g[0].trainees.all()
            for j in range(0, random.randint(1, min(len(ts),self.TG_MAX_SIZE))):
                pl = PerformedLesson.objects.create(
                    session=s,
                    lesson=random.choice(Lesson.objects.filter(
                        qualification=g[1], mode=mode,
                    )),
                    instructor=random.choice(instructors),
                    trainee=ts[j],
                )

        self.status_write('Generated {} sessions'.format(self.SS_COUNT))

    def generatePerformedLessons(self):
        instructors = MemberProfile.objects.filter(is_instructor_cached=True)
        def generateTraineePLs(trainee, qual, level=0.5, previous=False):
            # Theory
            ths = Lesson.objects.filter(qualification=qual, mode='TH')


    def generateTrips(self):
        for i in range(0, self.TRIP_COUNT):
            trip = Trip()

            trip.fake(fake=self.fake, quals=self.PERSONAL_QUALS, past=self.fake.boolean(chance_of_getting_true=80))

            if trip.min_qual == self.SD:
                trip.owner = random.choice(self.usefulUsersArray[6:]).get_profile()
            elif trip.min_qual == self.DL:
                trip.owner = random.choice(self.usefulUsersArray[8:]).get_profile()
            else:
                trip.owner = random.choice(self.usefulUsersArray).get_profile()

            trip.save()

        self.status_write('Generated {} trips'.format(self.TRIP_COUNT))

    def fillTrips(self):
        membership = MemberProfile.objects.filter(archived=False)
        trips_to_fill = Trip.objects.filter(state__gte=STATE_CANCELLED)
        for trip in trips_to_fill:
            if self.fake.boolean(chance_of_getting_true=10):
                continue
            if trip.spaces:
                fill_max = random.randint(0, trip.spaces + 5)
            else:
                fill_max = random.randint(0, 12)
            actors = [trip.owner.user] * 10 + [self.usefulUsers['do'], self.usefulUsers['su']]
            already_on_trip = []
            for i in range(0, fill_max):
                member = random.choice(membership)
                while member in already_on_trip:
                    member = random.choice(membership)

                already_on_trip.append(member)

                if trip.state in (STATE_COMPLETED, STATE_CANCELLED):
                    # Not allowed to do this via normal methods, do manually
                    TripMember.objects.create(
                        trip=trip,
                        member=member,
                        state=TripMember.STATE_ACCEPTED,
                    )
                else:
                    trip.add_members(members=[member], actor=random.choice(actors))


        self.status_write('Filled {} trips'.format(trips_to_fill.count()))

