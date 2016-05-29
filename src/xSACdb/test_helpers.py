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

    fixtures = settings.TEST_FIXTURES

    def setUp(self):
        self.setUp_user()

        # Hooks to allow precise setUp ordering
        if hasattr(self, 'setUp_base'):
            # For running this prior to test setup and request prefetch
            self.setUp_base()
        if hasattr(self, 'setUp_test'):
            # Individual tests setup, keep flat
            self.setUp_test()

    def setUp_base(self):
        pass

    def setUp_user(self):
        U = get_user_model()
        user = U.objects.create_user(
            email=self.EMAIL,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
        )
        user.save()
        user.memberprofile.new_notify = False
        user.memberprofile.save()
        self.user = user
        self.mp = user.memberprofile

    def get_random_date(self):
        return datetime.date.fromtimestamp(randrange(-2284101485, 2284101485))

    def get_future_date(self):
        dt = testdata.get_future_datetime()
        return datetime.date(dt.year, dt.month, dt.day)

    def create_a_user(self):
        """Make a random user, return them"""
        U = get_user_model()
        user = U.objects.create_user(
            first_name=testdata.get_name(name_count=1),
            last_name=testdata.get_name(name_count=1),
            email=testdata.get_email(),
            password=testdata.get_str(128),
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


class BaseAsGroupTest(BaseTest):
    # TODO migrate usage to AsGroupMixin and remove
    def setUp(self):
        super(BaseAsGroupTest, self).setUp()
        self.set_groups()

    def set_groups(self):
        for group in self.GROUPS:
            g = Group.objects.get(pk=group)
            self.user.groups.add(g)
        self.user.save()


class AsGroupMixin(object):
    def setUp_base(self):
        super(AsGroupMixin, self).setUp_base()
        self.set_groups()

    def set_groups(self):
        for group in self.GROUPS:
            g = Group.objects.get(pk=group)
            self.user.groups.add(g)
        self.user.save()


class ViewTestMixin(object):
    view = None
    url_name = None
    template_name = None
    allowed_unverified = False

    url_args = []
    url_kwargs = {}

    def get_url(self):
        if self.url_name:
            return reverse(self.url_name, args=self.url_args, kwargs=self.url_kwargs)
        else:
            return reverse(self.view, args=self.url_args, kwargs=self.url_kwargs)

    def get_template_name(self):
        if self.template_name:
            return self.template_name
        else:
            if hasattr(self.view, 'template_name'):
                return self.view.template_name
            else:
                raise ValueError("Provided view does not specify a template_name, you've gotta specify it in the test.")

    def get_response(self):
        client = self.get_client()
        response = client.get(self.get_url())
        return response

    @property
    def response(self):
        return self.get_response()

    def test_200(self):
        r = self.response
        self.assertEqual(200, r.status_code)

    def test_template_used(self):
        r = self.response
        self.assertTemplateUsed(r, self.get_template_name())

    def test_unverified(self):
        self.user.memberprofile.new_notify = True
        self.user.memberprofile.save()
        r = self.get_response() # Need a fresh response this time around
        if self.allowed_unverified:
            self.assertEqual(200, r.status_code)
        else:
            self.assertEqual(403, r.status_code)
