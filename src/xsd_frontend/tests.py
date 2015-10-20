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

class ClassicLogin(BaseTest):
    def test_login_username(self):
        # Correct login
        c=Client()
        self.assertTrue(c.login(username=self.user.username, password=self.PASSWORD))
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_login_email(self):
        # Correct login
        c=Client()
        self.assertTrue(c.login(username=self.EMAIL, password=self.PASSWORD))
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_login_username_incorrect(self):
        # Correct login
        c=Client()
        self.assertFalse(c.login(username=self.user.username, password=self.PASSWORD+"#"))
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_login_email_incorrect(self):
        # Correct login
        c=Client()
        self.assertFalse(c.login(username=self.EMAIL, password=self.PASSWORD+"#"))
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

class Dashboard(BaseTest):
    VIEW_NAME = 'dashboard'
    def test_200(self):
        self.assertEqual(self.get_page_status_code('dashboard'),200)
