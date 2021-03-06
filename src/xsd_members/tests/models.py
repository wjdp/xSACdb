

import datetime
import random

from xSACdb.test_helpers import BaseTest, BaseAsGroupTest
from xsd_members.models import MemberProfile, MembershipType
from xsd_training.models import Lesson, PerformedLesson, Qualification, PerformedQualification
from xsd_training.tests.base import TrainingTestToolsMixin


class BaseMemberTest(BaseTest):
    pass


class BaseMembersOfficerTest(BaseAsGroupTest):
    GROUPS = [6]


class MPFunc(BaseTest):
    # FIXME old test
    def test_u_mp_relationship(self):
        self.assertEqual(self.mp, self.user.memberprofile)

    def test_age(self):
        test_age = 21
        today = datetime.date.today()
        t_years_ago = datetime.date(
            year=(today.year - test_age),
            month=today.month,
            day=today.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(), test_age)


class MPExternalFunc(BaseTest):
    # FIXME old test
    def setUp(self):
        super(MPExternalFunc, self).setUp()
        self.make_pls()

    def make_pls(self):
        PLS = [
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO2', qualification__active=True),
                'completed': False,
                'partially_completed': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO3', qualification__active=True),
                'completed': True,
                'partially_completed': False,
                'public_notes': 'Note',
                'private_notes': 'Note',
            },
            {
                'trainee': self.mp,
                'lesson': Lesson.objects.get(code='OO4', qualification__active=True),
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
                trainee=PL['trainee'],
                lesson=PL['lesson'],
                completed=PL['completed'],
                partially_completed=PL['partially_completed'],
                public_notes=PL['public_notes'],
                private_notes=PL['private_notes'],
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
        self.setUpTestData()  # Class requires a new member profile for each test so we start with a clean slate

    def test_unicode(self):
        self.assertEqual(str(self.mp), "{} {}".format(self.FIRST_NAME, self.LAST_NAME))

    def test_award_qualification(self):
        pq = PerformedQualification(
            qualification=self.SD,
            mode='INT',
        )
        self.mp.award_qualification(pq, actor=self.mp.user)

        self.assertEqual(self.mp.top_qual_cached, self.SD)

    def test_top_qual(self):
        # User is new, has no quals
        self.assertIsNone(self.mp.top_qual())
        self.assertIsNone(self.mp.top_qual_cached)

        for qual in self.PERSONAL_QUALS:
            self.mp.set_qualification(qual)
            self.mp.save()
            self.assertEqual(self.mp.top_qual(), qual)

    def test_top_instructor_qual(self):
        # User is new, has no quals
        self.assertIsNone(self.mp.top_instructor_qual())
        self.assertIsNone(self.mp.top_qual_cached)

        for qual in self.INSTRUCTOR_QUALS:
            self.mp.set_qualification(qual)
            self.assertEqual(self.mp.top_instructor_qual(), qual)

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
        test_age = random.randrange(1, 2000)
        # Set DOB to test_age days ago, tomorrow
        a_date = datetime.date.today() + datetime.timedelta(days=1)
        t_years_ago = datetime.date(
            year=(a_date.year - test_age),
            month=a_date.month,
            day=a_date.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(), test_age - 1)

    def test_age_birthday(self):
        test_age = random.randrange(1, 2000)
        # Set DOB to test_age days ago, today
        today = datetime.date.today()
        t_years_ago = datetime.date(
            year=(today.year - test_age),
            month=today.month,
            day=today.day,
        )

        self.mp.date_of_birth = t_years_ago
        self.assertEqual(self.mp.age(), test_age)

    def test_formatted_methods(self):
        self.assertIsInstance(self.mp.formatted_address(), str)
        self.assertIsInstance(self.mp.formatted_other_qualifications(), str)
        self.assertIsInstance(self.mp.formatted_alergies(), str)

    def test_heshe(self):
        self.assertIsInstance(self.mp.heshe(), str)

    # TODO fix this test, self.mp seems to be deleted along with the PQs. I cannot reproduce this outside this test so am skipping for now
    # def test_remove_qualifications(self):
    #     self.mp.set_qualification(self.OD)
    #     self.mp.set_qualification(self.OWI)
    #     PerformedQualification.objects.filter(trainee=self).delete()
    #     self.mp.refresh_from_db()
    #     self.assertIsNone(self.mp.top_qual_cached)
    #     self.assertIsNone(self.mp.top_instructor_qual)

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
        self.mp.first_name = self.fake.first_name()
        self.mp.last_name = self.fake.last_name()
        self.mp.email = self.fake.email()
        self.mp.save()

        self.assertEqual(self.mp.first_name, self.user.first_name)
        self.assertEqual(self.mp.last_name, self.user.last_name)
        self.assertEqual(self.mp.email, self.user.email)

    def test_mp_get_missing_field_list(self):
        # We've filled all of them
        self.assertEqual(
            len(self.mp.get_missing_field_list()),
            0
        )

        # Remove one now
        self.mp.next_of_kin_name = ""
        self.mp.save()

        # There should be one less now
        self.assertEqual(
            len(self.mp.get_missing_field_list()),
            1
        )

    def test_mp_delete(self):
        # Bug #88, users are orphaned when their MP is deleted. Causes exceptions.
        mp_pk = self.mp.pk
        u_pk = self.user.pk
        self.mp.delete()
        # Check the MP is actually deleted
        self.assertEqual(MemberProfile.objects.filter(pk=mp_pk).count(), 0)
        # Check the associated user is also deleted
        self.assertEqual(self.User.objects.filter(pk=u_pk).count(), 0)

    def test_mp_approve(self):
        # Check that approving a member works
        self.mp.new_notify = True
        self.mp.save()
        self.mp.refresh_from_db()
        self.assertFalse(self.mp.verified)
        self.mp.approve(self.user)
        self.mp.refresh_from_db()
        self.assertTrue(self.mp.verified)

    def test_mp_archive(self):
        # Check that archiving member expunges and sets archived flag
        self.assertIsNot(self.mp.address, '')
        self.assertIsNot(self.mp.date_of_birth, None)
        self.assertFalse(self.mp.archived)
        self.mp.archive(self.user)
        self.mp.refresh_from_db()
        self.assertIs(self.mp.address, '')
        self.assertIs(self.mp.date_of_birth, None)
        self.assertTrue(self.mp.archived)

    def test_mp_reinstate(self):
        # Check that archiving member expunges and sets archived flag
        self.mp.archive(self.user)
        self.mp.refresh_from_db()
        self.assertTrue(self.mp.archived)
        self.mp.reinstate(self.user)
        self.mp.refresh_from_db()
        self.assertFalse(self.mp.archived)

    def test_mp_avatar(self):
        avatars = {
            'xs': self.mp.avatar_xs,
            'sm': self.mp.avatar_sm,
            'md': self.mp.avatar_md,
        }
        # Check they look like urls
        self.assertTrue('https' in self.mp.avatar_xs)
        self.assertTrue('https' in self.mp.avatar_sm)
        self.assertTrue('https' in self.mp.avatar_md)

        # Test the cache is invalidated
        self.mp.email = 'testytest@example.com'
        self.mp.save()
        # Check instance cache has been cleared, see #285
        self.assertNotEqual(avatars['xs'], self.mp.avatar_xs)
        self.assertNotEqual(avatars['sm'], self.mp.avatar_sm)
        self.assertNotEqual(avatars['md'], self.mp.avatar_md)
        # Check external cache has been cleared
        mp_fresh = MemberProfile.objects.get(pk=self.mp.pk)
        self.assertNotEqual(avatars['xs'], mp_fresh.avatar_xs)
        self.assertNotEqual(avatars['sm'], mp_fresh.avatar_sm)
        self.assertNotEqual(avatars['md'], mp_fresh.avatar_md)


class MembershipTypeTest(BaseTest):
    def test_unicode(self):
        NAME = self.fake.name()
        a = MembershipType.objects.create(name=NAME)
        a.save()
        self.assertEqual(a.name, str(a))


class MembershipManagerTest(BaseTest):
    def test_all(self):
        u = self.create_a_user()
        self.assertTrue(u.memberprofile in MemberProfile.objects.all())

    def test_hidden(self):
        u = self.create_a_user()
        u.memberprofile.hidden = True
        u.memberprofile.save()
        self.assertFalse(u.memberprofile in MemberProfile.objects.all())
