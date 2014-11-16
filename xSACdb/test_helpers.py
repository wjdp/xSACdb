from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.core.urlresolvers import reverse

class BaseTest(TestCase):
    USERNAME = 'billy'
    PASSWORD = 'billy1234'
    EMAIL = 'billy_is_cool@example.com'
    FIRST_NAME = 'Billy'
    LAST_NAME = 'Bloggs'

    fixtures = settings.TEST_FIXTURES

    def setUp(self):
        self.setUp_user()

    def setUp_user(self):
        U = get_user_model()
        user = U.objects.create_user(
            email = self.EMAIL,
            password = self.PASSWORD,
            first_name = self.FIRST_NAME,
            last_name = self.LAST_NAME,
        )
        user.save()
        self.user = user

    def login(self, c):
        """Login a client with USERNAME"""
        c.login(username=self.user.username, password=self.PASSWORD)
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

class BaseAsGroupTest(BaseTest):
    def setUp(self):
        super(BaseAsGroupTest, self).setUp()
        self.set_groups()
    def set_groups(self):
        for group in self.GROUPS:
            g = Group.objects.get(pk=group)
            self.user.groups.add(g)
        self.user.save()

class BaseTrainingTest(BaseAsGroupTest):
    GROUPS=[3]
