import datetime
import random
import testdata

from xSACdb.test_helpers import BaseTest, BaseAsGroupTest

from xsd_members.models import MemberProfile, MembershipType
from xsd_training.models import Lesson, PerformedLesson, Qualification

from xsd_training.tests.base import TrainingTestToolsMixin

class BaseMemberTest(BaseTest):
    pass

class BaseMembersOfficerTest(BaseAsGroupTest):
    GROUPS=[6]

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

class MemberProfileTest(BaseMemberTest, TrainingTestToolsMixin):
    def setUp(self):
        super(MemberProfileTest, self).setUp()
        self.trainingTestToolsSetUp()

    def test_unicode(self):
        self.assertEqual(unicode(self.mp), u"{} {}".format(self.FIRST_NAME, self.LAST_NAME))

    def test_top_qual(self):
        # User is new, has no quals
        self.assertIsNone(self.mp.top_qual())
        self.assertIsNone(self.mp.top_qual_cached)

        # Iterate over them in reverse
        for qual in self.PERSONAL_QUALS[::-1]:
            self.mp.set_qualification(qual)
            self.mp.save()
            self.assertEqual(self.mp.top_qual(), qual)

        # Iterate over them in forward
        for qual in self.PERSONAL_QUALS:
            self.mp.set_qualification(qual)
            self.mp.save()
            self.assertEqual(self.mp.top_qual(), qual)


    def test_top_instructor_qual(self):
        # User is new, has no quals
        self.assertIsNone(self.mp.top_instructor_qual())
        self.assertIsNone(self.mp.top_qual_cached)

        # Iterate over them in reverse
        for qual in self.INSTRUCTOR_QUALS[::-1]:
            self.mp.set_qualification(qual)
            self.mp.save()
            self.assertEqual(self.mp.top_instructor_qual(), qual)

        # Iterate over them in forward
        for qual in self.INSTRUCTOR_QUALS:
            self.mp.set_qualification(qual)
            self.mp.save()
            # TODO Because of some instructor quals being at same level
            # (PI and TI) this is commented out for now
            # self.assertEqual(self.mp.top_instructor_qual(), qual)

    def test_is_instructor(self):
        self.assertFalse(self.mp.is_instructor())

        # Iterate over them in reverse
        for qual in self.INSTRUCTOR_QUALS[::-1]:
            self.mp.set_qualification(qual)
            self.mp.save()
            self.assertTrue(self.mp.is_instructor())


    def test_club_expired(self):
        self.assertTrue(self.mp.club_expired())
        # Set future
        self.mp.club_expiry = self.get_future_date()
        self.mp.save()
        self.assertFalse(self.mp.club_expired())
        # Set today
        self.mp.club_expiry = datetime.date.today()
        self.mp.save()
        self.assertTrue(self.mp.club_expired())


    def test_bsac_expired(self):
        self.assertTrue(self.mp.bsac_expired())
        # Set future
        self.mp.bsac_expiry = self.get_future_date()
        self.mp.save()
        self.assertFalse(self.mp.bsac_expired())
        # Set today
        self.mp.bsac_expiry = datetime.date.today()
        self.mp.save()
        self.assertTrue(self.mp.bsac_expired())

    def test_medical_form_expired(self):
        self.assertTrue(self.mp.medical_form_expired())
        # Set future
        self.mp.medical_form_expiry = self.get_future_date()
        self.mp.save()
        self.assertFalse(self.mp.medical_form_expired())
        # Set today
        self.mp.medical_form_expiry = datetime.date.today()
        self.mp.save()
        self.assertTrue(self.mp.medical_form_expired())

    def test_no_expiry_data(self):
        self.assertTrue(self.mp.no_expiry_data())
        self.mp.medical_form_expiry = self.get_future_date()
        self.assertFalse(self.mp.no_expiry_data())

    def test_membership_problem(self):
        self.assertTrue(self.mp.membership_problem())
        self.mp.club_expiry = self.get_future_date()
        self.mp.bsac_expiry = self.get_future_date()
        self.assertTrue(self.mp.membership_problem())
        self.mp.medical_form_expiry = self.get_future_date()
        self.assertFalse(self.mp.membership_problem())

    # def test_performed_lesson_ramble(self):
    #     done in old test suite above
    #     pass

    def test_date_of_birth(self):
        # dob is an alias function, bit silly, test it
        date = self.get_future_date()
        self.mp.date_of_birth = date
        self.mp.save()
        self.assertEqual(self.mp.dob(), date)

    def test_no_date_of_birth(self):
        self.mp.date_of_birth = None
        self.mp.save()
        self.assertIsNone(self.mp.age())

    def test_age_prior_birthday(self):
        test_age = random.randrange(1,2000)
        # Set DOB to test_age days ago, tomorrow
        a_date = datetime.date.today() + datetime.timedelta(days=1)
        t_years_ago =  datetime.date(
            year = (a_date.year-test_age),
            month = a_date.month,
            day = a_date.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(),test_age-1)

    def test_age_birthday(self):
        test_age = random.randrange(1,2000)
        # Set DOB to test_age days ago, today
        today = datetime.date.today()
        t_years_ago =  datetime.date(
            year = (today.year-test_age),
            month = today.month,
            day = today.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(),test_age)

    def test_formatted_methods(self):
        self.assertIsInstance(self.mp.formatted_address(), basestring)
        self.assertIsInstance(self.mp.formatted_other_qualifications(), basestring)
        self.assertIsInstance(self.mp.formatted_alergies(), basestring)

    def test_heshe(self):
        self.assertEqual(self.mp.heshe(), "They")

    def test_remove_qualifications(self):
        self.mp.set_qualification(self.OD)
        self.mp.set_qualification(self.OWI)
        self.mp.save()
        self.mp.remove_qualifications()
        self.mp.save()
        self.assertIsNone(self.mp.top_qual())
        self.assertEqual(self.mp.top_instructor_qual(), self.OWI)

    def test_remove_qualifications_instructor(self):
        self.mp.set_qualification(self.OD)
        self.mp.set_qualification(self.OWI)
        self.mp.save()
        self.mp.remove_qualifications(instructor=True)
        self.mp.save()
        self.assertIsNone(self.mp.top_instructor_qual())
        self.assertEqual(self.mp.top_qual(), self.OD)

    def test_add_sdc(self):
        self.mp.add_sdc(self.BOAT_HANDLING)
        self.mp.add_sdc(self.BOAT_HANDLING)
        self.mp.add_sdc(self.WRECK_APPRECIATION)
        self.assertEqual(self.mp.sdcs.count(), 2)
        self.assertTrue(self.BOAT_HANDLING in self.mp.sdcs.all())
        self.assertTrue(self.WRECK_APPRECIATION in self.mp.sdcs.all())

    def test_upcoming_sdcs(self):
        # Should be blank
        self.assertEqual(len(self.mp.upcoming_sdcs()), 0)
        # TODO test properly

    def test_user_transfers(self):
        self.assertEqual(self.mp.memberprofile(), self.mp)
        self.assertEqual(self.mp.get_full_name(), self.user.get_full_name())
        self.assertEqual(self.mp.date_joined(), self.user.date_joined)

    def test_training_for(self):
        self.assertIsNone(self.mp.training_for)
        # compute_training_for
        pl1 = self.create_basic_pl(trainee=self.mp)
        self.assertIsNone(self.mp.training_for)

        # Save first lesson as OO1
        pl1.lesson = self.OO1
        pl1.save()

        # Save second as SO1, thfr training_for should be Sports
        pl2 = self.create_basic_pl(trainee=self.mp)
        pl2.lesson = self.SO1
        pl2.save()

        self.assertEqual(self.mp.compute_training_for(), self.SD)

        self.assertEqual(self.mp.training_for, self.SD)

    def test_mp_sync(self):
        self.mp.first_name = testdata.get_name(name_count=1)
        self.mp.last_name = testdata.get_name(name_count=1)
        self.mp.email = testdata.get_email()
        self.mp.save()

        self.assertEqual(self.mp.first_name, self.user.first_name)
        self.assertEqual(self.mp.last_name, self.user.last_name)
        self.assertEqual(self.mp.email, self.user.email)

    def test_mp_get_missing_field_list(self):
        # We've not filled any of them
        self.assertEqual(
            len(self.mp.get_missing_field_list()),
            len(self.mp.REQUIRED_FIELDS)
        )

        # Fill one in now
        self.mp.next_of_kin_name = "Mary"
        self.mp.save()

        # There should be one less now
        self.assertEqual(
            len(self.mp.get_missing_field_list()),
            len(self.mp.REQUIRED_FIELDS)-1
        )

class MembershipTypeTest(BaseTest):
    def test_unicode(self):
        NAME = testdata.get_str(40)
        a = MembershipType.objects.create(name=NAME)
        a.save()
        self.assertEqual(a.name, unicode(a))


class MembershipManagerTest(BaseTest):
    def test_all(self):
        u = self.create_a_user()
        self.assertTrue(u.memberprofile in MemberProfile.objects.all())

    def test_hidden(self):
        u = self.create_a_user()
        u.memberprofile.hidden = True
        u.memberprofile.save()
        self.assertFalse(u.memberprofile in MemberProfile.objects.all())
