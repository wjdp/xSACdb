import datetime

from django.conf import settings

from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model

from xsd_members.models import MemberProfile
from xsd_training.models import Lesson, PerformedLesson

class PresetUser(TestCase):
    USERNAME = 'bob'
    EMAIL = 'bob@example.com'
    PASSWORD = 'correcthorsebatterystaple'

    fixtures = settings.TEST_FIXTURES

    def setUp(self):
        self.make_user()
        self.make_pls()

    def make_user(self):
        U = get_user_model()
        self.u = U.objects.create_user(
            email=self.EMAIL,
            password=self.PASSWORD,
            first_name='Bob',
            last_name='Blobby',
        )

        self.u.save()

        self.mp = self.u.memberprofile
        self.mp.save()

    def get_logged_in_client(self):
        c = Client()
        res = c.post('/accounts/login/', {'username':self.EMAIL, 'password':self.PASSWORD})
        return c

    def make_pls(self):
        PLS = [
            {
                'trainee': self.u.memberprofile,
                'lesson': Lesson.objects.get(code='OO3'),
                'completed': False,
                'partially_complted': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.u.memberprofile,
                'lesson': Lesson.objects.get(code='OO3'),
                'completed': True,
                'partially_complted': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.u.memberprofile,
                'lesson': Lesson.objects.get(code='OO3'),
                'completed': False,
                'partially_complted': True,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.u.memberprofile,
                'lesson': None,
                'completed': False,
                'partially_complted': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.u.memberprofile,
                'lesson': None,
                'completed': False,
                'partially_complted': False,
                'public_notes': '',
                'private_notes': '',
            }
        ]
        for PL in PLS:
            new_pl = PerformedLesson()
            new_pl.trainee = PL['trainee']
            new_pl.lesson = PL['lesson']
            new_pl.completed = PL['completed']
            new_pl.partially_complted = PL['partially_complted']
            new_pl.public_notes = PL['public_notes']
            new_pl.private_notes = PL['private_notes']
            new_pl.save()

class PresetAdminUser(PresetUser):
    def setUp(self):
        super(PresetAdminUser, self).setUp()
        self.make_admin()
    def make_admin(self):
        g = Group.objects.get(pk=2)
        self.u.groups.add(g)
        self.u.save()

class MPFunctionality(PresetUser):

    def test_u_mp_relationship(self):
        self.assertEqual(self.mp, self.u.memberprofile)

    def test_age(self):
        test_age = 21
        today = datetime.date.today()
        t_years_ago =  datetime.date(
            year = (today.year-test_age),
            month = today.month,
            day = today.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(),test_age)

    def test_personal_fields(self):
        # We have missing personal fields
        self.assertEqual(self.mp.missing_personal_details(), True)
        # Set all of them
        self.mp.address='Demo address'
        self.mp.postcode='P0ST CDE'
        self.mp.home_phone='555-SEXY'
        self.mp.mobile_phone='07123456789'
        self.mp.next_of_kin_name='Mary Flobby'
        self.mp.next_of_kin_relation='Mother dearest'
        self.mp.next_of_kin_phone='01234 567890'
        self.mp.save()
        # We now shouldn't have any
        self.assertEqual(self.mp.missing_personal_details(), False)

    def test_performed_lesson_ramble(self):
        out = self.mp.performed_lesson_ramble()
        self.assertTrue('OO3' in out)

    def test_caching(self):
        pass
