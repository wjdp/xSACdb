import datetime
import random

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

    @classmethod
    def setUpTestData(cls):
        cls.setUp_user()

        # Hooks to allow precise setUp ordering
        if hasattr(cls, 'setUp_base'):
            # For running this prior to test setup and request prefetch
            cls.setUp_base()
        if hasattr(cls, 'setUp_test'):
            # Individual tests setup, keep flat
            cls.setUp_test()

    @classmethod
    def setUp_base(cls):
        pass

    @classmethod
    def setUp_user(cls):
        U = get_user_model()
        user = U.objects.create_user(
            email=cls.EMAIL,
            password=cls.PASSWORD,
            first_name=cls.FIRST_NAME,
            last_name=cls.LAST_NAME,
        )
        user.save()
        user.memberprofile.new_notify = False
        user.memberprofile.date_of_birth = cls.get_past_date()
        user.memberprofile.gender = random.choice(('m', 'f'))
        user.memberprofile.address = "addr line 1\naddr line 2"
        user.memberprofile.postcode = "UHU ioIJ"
        user.memberprofile.home_phone = "8219038210938"
        user.memberprofile.mobile_phone = "8219031232138"
        user.memberprofile.next_of_kin_name = testdata.get_name(2)
        user.memberprofile.next_of_kin_relation = testdata.get_name(1)
        user.memberprofile.next_of_kin_phone = "4684564564654564"
        user.memberprofile.save()
        cls.user = user
        cls.mp = user.memberprofile

    @staticmethod
    def get_random_date():
        return datetime.date.fromtimestamp(random.randrange(-2284101485, 2284101485))

    @staticmethod
    def get_future_date():
        dt = testdata.get_future_datetime()
        return datetime.date(dt.year, dt.month, dt.day)

    @staticmethod
    def get_past_date():
        dt = testdata.get_past_datetime()
        return datetime.date(max(1900, dt.year), dt.month, dt.day)

    @staticmethod
    def create_a_user():
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
        return self.login(self.client)


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
    @classmethod
    def setUp_base(cls):
        super(AsGroupMixin, cls).setUp_base()
        cls.set_groups()

    @classmethod
    def set_groups(cls):
        for group in cls.GROUPS:
            g = Group.objects.get(pk=group)
            cls.user.groups.add(g)
        cls.user.save()


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
