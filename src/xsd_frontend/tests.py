from unittest.mock import patch

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from faker import Factory

from xSACdb import version
from xSACdb.test_helpers import BaseTest, ViewTestMixin
from xsd_auth.models import User

fake = Factory.create(settings.FAKER_LOCALE)
fake.seed(settings.RANDOM_SEED)


class AccountsLogin(TestCase):
    def test_200(self):
        c = Client()
        r = c.get('/accounts/login/')
        self.assertEqual(r.status_code, 200)


class RegisterLogin(TestCase):
    def test_200(self):
        c = Client()
        r = c.get('/accounts/register/')
        self.assertEqual(r.status_code, 200)

    def test_register_form(self):
        c = Client()
        password = fake.password()
        post_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': password,
        }
        c.post('/accounts/register/', post_data)

        # Check user exists
        self.assertEqual(User.objects.filter(email=post_data['email']).count(), 1)

        # Check user creation
        u = User.objects.get(email=post_data['email'])
        self.assertEqual(u.first_name, post_data['first_name'])
        self.assertEqual(u.last_name, post_data['last_name'])
        self.assertEqual(u.email, post_data['email'])

        # Check profile creation
        self.assertEqual(u.memberprofile.first_name, post_data['first_name'])
        self.assertEqual(u.memberprofile.last_name, post_data['last_name'])
        self.assertEqual(u.memberprofile.email, post_data['email'])


class ClassicLogin(TestCase):
    USERNAME = fake.user_name()
    FIRST_NAME = fake.first_name()
    LAST_NAME = fake.last_name()
    EMAIL = fake.email()
    PASSWORD = fake.password()

    def setUp(self):
        self.user = User.objects.create_user(
            username=self.USERNAME,
            email=self.EMAIL,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
        )
        self.user.save()

        # Clear cached state of newbie form, cache is shared between tests
        cache.delete('newbie_form_bypass_{}'.format(self.user.pk))

    def test_login_username(self):
        # Correct login with username
        c = self.client
        self.assertTrue(c.login(username=self.user.username, password=self.PASSWORD))
        # Should be redirect
        response = c.get(reverse('xsd_frontend:dashboard'))
        self.assertEqual(response.status_code, 302)
        # To update profile view
        response = c.get(reverse('xsd_members:MemberProfileUpdate'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_login_email(self):
        # Correct login with email
        c = self.client
        self.assertTrue(c.login(username=self.EMAIL, password=self.PASSWORD))
        # Should be redirect
        response = c.get(reverse('xsd_frontend:dashboard'))
        self.assertEqual(response.status_code, 302)
        # To update profile view
        response = c.get(reverse('xsd_members:MemberProfileUpdate'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    # Weird postgres error #214, disabled test as username fail isn't really in scope of app tests
    # def test_login_username_incorrect(self):
    #     # Invalid login
    #     c = Client()
    #     self.assertFalse(c.login(username=self.user.username, password=testdata.get_str(128)))
    #     response = c.get(reverse('xsd_frontend:dashboard'))
    #     self.assertEqual(response.status_code, 302)

    def test_login_email_incorrect(self):
        # Invalid login
        c = Client()
        self.assertFalse(c.login(username=self.EMAIL, password=fake.password()))
        response = c.get(reverse('xsd_frontend:dashboard'))
        self.assertEqual(response.status_code, 302)


class Dashboard(ViewTestMixin, BaseTest):
    url_name = 'xsd_frontend:dashboard'
    template_name = 'frontend/dashboard.html'
    allowed_unverified = True


# Tests for xSACdb module environment
# Doesn't feel the best place for tests for this. Due to I don't think django can run tests outside of apps.

class VersionGetVersion(TestCase):
    def test_empty(self):
        with patch.dict('os.environ', {'VCS_REV': ''}):
            self.assertIsNone(version.get_version())

    def test_present(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-26-gea9f8a4'}):
            self.assertEqual(version.get_version(), 'v0.8.0-26-gea9f8a4')


class VersionGetRelease(TestCase):
    def test_empty(self):
        with patch.dict('os.environ', {'VCS_REV': ''}):
            self.assertIsNone(version.get_release())

    def test_bare(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0'}):
            self.assertEqual(version.get_release(), 'v0.8.0')

    def test_with_tail(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-26-gea9f8a4'}):
            self.assertEqual(version.get_release(), 'v0.8.0')

    def test_with_rc(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-rc1'}):
            self.assertEqual(version.get_release(), 'v0.8.0-rc1')

    def test_with_rc_and_tail(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-rc1-26-gea9f8a4'}):
            self.assertEqual(version.get_release(), 'v0.8.0-rc1')


class VersionGetSentryRelease(TestCase):
    def test_empty(self):
        with patch.dict('os.environ', {'VCS_REV': ''}):
            self.assertIsNone(version.get_sentry_release())

    def test_bare(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0'}):
            self.assertEqual(version.get_sentry_release(), 'xsacdb@0.8.0')

    def test_with_tail(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-26-gea9f8a4'}):
            self.assertEqual(version.get_sentry_release(), 'xsacdb@0.8.0')

    def test_with_rc(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-rc1'}):
            self.assertEqual(version.get_sentry_release(), 'xsacdb@0.8.0-rc1')

    def test_with_rc_and_tail(self):
        with patch.dict('os.environ', {'VCS_REV': 'v0.8.0-rc1-26-gea9f8a4'}):
            self.assertEqual(version.get_sentry_release(), 'xsacdb@0.8.0-rc1')
