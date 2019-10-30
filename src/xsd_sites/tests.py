import random

from xSACdb.test_helpers import BaseTest
from xsd_sites.models import *

from django.conf import settings
from faker import Factory

fake = Factory.create(settings.FAKER_LOCALE)
fake.seed(settings.RANDOM_SEED)

class SiteTestToolsMixin:
    def create_site(self):
        site = Site.objects.create(
            name=fake.name(),
            type=random.choice(SITE_TYPES)[0],
        )
        site.save()
        return site

class SiteTest(BaseTest):
    def test_unicode(self):
        name = fake.name()
        site = Site.objects.create(
            name=name,
            type=random.choice(SITE_TYPES)[0],
        )
        site.save()

        self.assertIsInstance(str(site), str)
        self.assertEqual(str(site), name)
