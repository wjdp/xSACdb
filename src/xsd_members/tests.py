import datetime

from django.conf import settings

from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model

from xSACdb.test_helpers import *

from xsd_members.models import MemberProfile
from xsd_training.models import Lesson, PerformedLesson, Qualification

class MPFunc(BaseTest):

    def test_u_mp_relationship(self):
        self.assertEqual(self.mp, self.user.memberprofile)

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
        self.mp.next_of_kin_name='Mary Bloggs'
        self.mp.next_of_kin_relation='Mother dearest'
        self.mp.next_of_kin_phone='01234 567890'
        self.mp.save()
        # We now shouldn't have any
        self.assertEqual(self.mp.missing_personal_details(), False)

    def test_caching(self):
        pass

class MPExternalFunc(BaseTest):
    def setUp(self):
        super(MPExternalFunc, self).setUp()
        self.make_pls()
    def make_pls(self):
        PLS = [
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO2'),
                'completed': False,
                'partially_completed': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO3'),
                'completed': True,
                'partially_completed': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO4'),
                'completed': False,
                'partially_completed': True,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': None,
                'completed': False,
                'partially_completed': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': None,
                'completed': False,
                'partially_completed': False,
                'public_notes': '',
                'private_notes': '',
            }
        ]
        for PL in PLS:
            new_pl = PerformedLesson(
                trainee = PL['trainee'],
                lesson = PL['lesson'],
                completed = PL['completed'],
                partially_completed = PL['partially_completed'],
                public_notes = PL['public_notes'],
                private_notes = PL['private_notes'],
            )
            new_pl.save()

    def test_performed_lesson_ramble(self):
        self.assertTrue(PerformedLesson.objects.get_lessons(
            trainee=self.mp).count() > 3)
        out = self.mp.performed_lesson_ramble()
        self.assertTrue(('OO2' in out) and ('OO3' in out) and
            ('OO4' in out))

    def test_training_for(self):
        # Crosses over into xsd_training.models.Qualification
        # Checks the MemberProfile.update_training_for
        # and the PerformedLesson save hook

        ocean_diver = Qualification.objects.get(code='OD')
        self.assertTrue(self.mp.training_for == ocean_diver)

