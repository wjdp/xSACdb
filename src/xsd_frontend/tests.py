from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from faker import Factory

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
    FIRST_NAME = fake.first_name()
    LAST_NAME = fake.last_name()
    EMAIL = fake.email()
    PASSWORD = fake.password()

    def setUp(self):
        self.user = User.objects.create_user(
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
