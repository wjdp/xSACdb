"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

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
