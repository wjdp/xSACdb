import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from xsd_members.models import MemberProfile

class MPFunctionality(TestCase):
    def test_create_user(self):
        self.u = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='correcthorsebatterystaple',
        )
        self.u.first_name='Bob'
        self.u.last_name='Blobby'
        self.u.save()

        self.mp = self.u.memberprofile
        self.mp.save()

        self.assertEqual(self.mp, self.u.memberprofile)

    def test_age(self):
        self.test_create_user()

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
        self.test_create_user()
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


    def test_caching(self):
        pass
