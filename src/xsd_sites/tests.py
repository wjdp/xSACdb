import random

from django.test import TestCase
from xsd_sites.models import *

import testdata


class SiteTestToolsMixin(object):
    def create_site(self):
        site = Site.objects.create(
            name=testdata.get_str(128),
            type=random.choice(SITE_TYPES),
        )
        site.save()
        return site

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
