from __future__ import unicode_literals

import random

from xSACdb.test_helpers import BaseTest
from xsd_sites.models import *

import testdata

class SiteTestToolsMixin(object):
    def create_site(self):
        site = Site.objects.create(
            name=testdata.get_str(128),
            type=random.choice(SITE_TYPES)[0],
        )
        site.save()
        return site

class SiteTest(BaseTest):
    def test_unicode(self):
        name = testdata.get_str(128)
        site = Site.objects.create(
            name=name,
            type=random.choice(SITE_TYPES)[0],
        )
        site.save()

        self.assertIsInstance(unicode(site), basestring)
        self.assertEqual(unicode(site), name)
