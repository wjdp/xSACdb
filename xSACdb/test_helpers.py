from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

class BaseTest(TestCase):
    USERNAME = 'billy'
    PASSWORD = 'billy1234'
    EMAIL = 'billy_is_cool@example.com'
    FIRST_NAME = 'Billy'
    LAST_NAME = 'Bloggs'

    def setUp(self):
        self.setUp_user()

    def setUp_user(self):
        user = User.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)
        user.first_name=self.FIRST_NAME
        user.last_name=self.LAST_NAME
        user.save()
        self.user = user

    def login(self, c):
        """Login a client with USERNAME"""
        c.login(username=self.USERNAME, password=self.PASSWORD)
        return c

    def get_client(self):
        """Return a logged in and ready to go client"""
        c = Client()
        return self.login(c)

    def get_page_status_code(self, view_name=None, kwargs=None):
        if not view_name:
            view_name = self.VIEW_NAME
        c = self.get_client()

        response = c.get(reverse(view_name, kwargs=kwargs))
        return response.status_code
