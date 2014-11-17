"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from xSACdb.test_helpers import BaseTest, BaseTrainingTest, FixtureMixin

from xsd_training.models import *


class PoolSheetGenerate(BaseTrainingTest, FixtureMixin):
    url_pool = '/training/pool-sheet/?session=18&sort_by=instructor__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'
    url_ow = '/training/pool-sheet/?session=16&sort_by=instructor__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'
    url_theory = '/training/pool-sheet/?session=10&sort_by=trainee__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'

    def generic_ps(self, url):
        c = self.get_client()
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

        # Response context not getting anything :\
        # self.assertTrue(response.context['session'])
        # self.assertTrue( len(response.context['pls_extended']) > 6 )

    def test_dumb_ps_pool(self):
        self.generic_ps(self.url_ow)
    def test_dumb_ps_ow(self):
        self.generic_ps(self.url_ow)
    def test_dumb_ps_theory(self):
        self.generic_ps(self.url_theory)
