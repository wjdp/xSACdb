from __future__ import absolute_import
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import authenticate
import testdata

from xSACdb.test_helpers import BaseTest
from xsd_auth.models import User
from xsd_members.models import MemberProfile


class UserTest(TestCase):
    FIRST_NAME = testdata.get_name(name_count=1)
    LAST_NAME = testdata.get_name(name_count=1)
    EMAIL = testdata.get_email()
    PASSWORD = testdata.get_str(128)

    def create_user(self):
        user = User.objects.create_user(
                first_name=self.FIRST_NAME,
                last_name=self.LAST_NAME,
                email=self.EMAIL,
                password=self.PASSWORD
        )
        user.save()
        return user

    def test_create_user(self):
        user = self.create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, self.FIRST_NAME)
        self.assertEqual(user.last_name, self.LAST_NAME)
        self.assertEqual(user.email, self.EMAIL)
        self.assertTrue(len(user.password) > 0)

    def test_username_authentication(self):
        user_a = self.create_user()
        user_b = authenticate(
            username=user_a.username,
            password=self.PASSWORD,
        )
        self.assertEqual(user_a, user_b)

    def test_email_authentication(self):
        user_a = self.create_user()
        user_b = authenticate(
            username=self.EMAIL,
            password=self.PASSWORD,
        )
        self.assertEqual(user_a, user_b)

    def test_full_name(self):
        user = self.create_user()
        self.assertEqual(user.get_full_name(), u"{0} {1}".format(
            self.FIRST_NAME, self.LAST_NAME
        ))

    def test_get_short_name(self):
        user = self.create_user()
        self.assertEqual(user.get_short_name(), self.FIRST_NAME)

    def test_first_name(self):
        user = self.create_user()
        self.assertEqual(user.get_first_name(), self.FIRST_NAME)

    def test_last_name(self):
        user = self.create_user()
        self.assertEqual(user.get_last_name(), self.LAST_NAME)

    def test_email_user(self):
        user = self.create_user()
        user.email_user('subject', 'message', 'from@example.com')

    def test_get_profile(self):
        user = self.create_user()
        self.assertIsInstance(user.get_profile(), MemberProfile)

    def test_profile_image_url(self):
        user = self.create_user()
        self.assertIsInstance(user.profile_image_url(), basestring)

    def test_unicode(self):
        user = self.create_user()
        self.assertEqual(unicode(user), user.get_full_name())


class PasswordChangeViewTest(BaseTest):
    def test200(self):
        self.assertEqual(self.get_page_status_code('xsd_auth:account_change_password'), 200)
    # TODO test password change


class SocialAccountConnectionsViewTest(BaseTest):
    def test200(self):
        self.assertEqual(self.get_page_status_code('xsd_auth:socialaccount_connections'), 200)
    # TODO test more
