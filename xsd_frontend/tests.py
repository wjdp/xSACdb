from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse

from xSACdb.test_helpers import BaseTest

class AccountsLogin(TestCase):
    def test_login_form_alive(self):
        c=Client()
        response = c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)


class RegisterLogin(TestCase):
    def test_register_form_alive(self):
        c=Client()
        response = c.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

class ClassicLogin(TestCase):
    USERNAME = 'billy'
    PASSWORD = 'billy1234'
    EMAIL = 'billy_is_cool@example.com'

    def setUp(self):
        U = get_user_model()
        user = U.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)
        user.save()
        self.user = user

    def test_login_username(self):
        # Correct login
        c=Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_login_email(self):
        # Correct login
        c=Client()
        c.login(username=self.EMAIL, password=self.PASSWORD)
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_login_username_incorrect(self):
        # Correct login
        c=Client()
        c.login(username=self.USERNAME, password=self.PASSWORD+".")
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_login_email_incorrect(self):
        # Correct login
        c=Client()
        c.login(username=self.EMAIL, password=self.PASSWORD+".")
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

class Dashboard(BaseTest):
    VIEW_NAME = 'dashboard'
    def test_200(self):
        self.assertEqual(self.get_page_status_code(''),200)
