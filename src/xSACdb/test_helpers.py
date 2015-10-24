import datetime
from random import randrange

from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.core.urlresolvers import reverse

import testdata

class BaseTest(TestCase):
    FIRST_NAME = testdata.get_name(name_count=1)
    LAST_NAME = testdata.get_name(name_count=1)
    EMAIL = testdata.get_email()
    PASSWORD = testdata.get_str(128)

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
        self.mp = user.memberprofile

    def get_random_date(self):
        return datetime.date.fromtimestamp(randrange(-2284101485, 2284101485))

    def create_a_user(self):
        """Make a random user, return them"""
        U = get_user_model()
        user = U.objects.create_user(
            first_name = testdata.get_name(name_count=1),
            last_name = testdata.get_name(name_count=1),
            email = testdata.get_email(),
            password = testdata.get_str(128),
        )
        user.save()
        return user

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

    def assert200(self, url):
        c = self.get_client()
        response = c.get(url)
        self.assertEqual(response.status_code, 200)


class BaseAsGroupTest(BaseTest):
    fixtures = ['groups']
    def setUp(self):
        super(BaseAsGroupTest, self).setUp()
        self.set_groups()
    def set_groups(self):
        for group in self.GROUPS:
            g = Group.objects.get(pk=group)
            self.user.groups.add(g)
        self.user.save()

class FixtureMixin(object):
    fixtures = settings.TEST_FIXTURES
