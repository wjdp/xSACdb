from __future__ import unicode_literals

import random

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

from xSACdb.roles.groups import GROUP_TRIPS
from xSACdb.test_helpers import BaseTest
from xsd_auth.models import User
from xsd_frontend.tests import fake
from xsd_trips.models import Trip


class BaseTripTest(BaseTest):
    def setUp(self):
        self.member = User.objects.fake_single(self.fake)
        self.trip_organiser = User.objects.fake_single(self.fake)
        self.do = User.objects.fake_single(self.fake)
        self.do.groups.add(Group.objects.get(pk=GROUP_TRIPS))

        self.new_trip = self.create_a_trip()
        self.open_trip = self.create_a_trip()
        self.open_trip.set_approved(self.do)
        self.open_trip.set_open(self.do)

    def create_a_trip(self):
        return Trip.objects.create(
            name=self.fake.name(),
            date_start=self.fake.date_time_between(start_date='now', end_date='+10y').date(),
            description='\n\n'.join(fake.paragraphs(nb=random.randrange(1, 4))),
            owner=self.trip_organiser.profile,
        )


class TripManagerTest(BaseTripTest):
    def test_upcoming_hidden(self):
        # Test a trip that hasn't been approved yet doesn't show up in the 'upcoming' list
        self.assertFalse(self.new_trip in Trip.objects.upcoming())

    def test_upcoming_hidden_all(self):
        # Test a trip that hasn't been approved yet does show up in upcoming all
        self.assertTrue(self.new_trip in Trip.objects.upcoming_all())

    def test_upcoming_open(self):
        # Test an open trip shows in upcoming
        self.assertTrue(self.open_trip in Trip.objects.upcoming())

    def test_private(self):
        # New trips show in private
        self.assertTrue(self.new_trip in Trip.objects.private())


class TripStateTest(BaseTripTest):
    def test_state_class(self):
        self.assertEqual(self.new_trip.state_class, 'trip-state-new')

    def test_deny_trip(self):
        # Member / trip owner cannot deny
        self.assertFalse(self.new_trip.is_denied)
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_approved(self.member)
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_denied(self.trip_organiser)

        # DO can
        self.new_trip.set_denied(self.do)
        self.new_trip.refresh_from_db()
        self.assertTrue(self.new_trip.is_denied)

    def test_approve_trip(self):
        # Member / trip owner cannot approve
        self.assertFalse(self.new_trip.is_approved)
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_approved(self.member)
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_approved(self.trip_organiser)

        # DO can
        self.new_trip.set_approved(self.do)
        self.new_trip.refresh_from_db()
        self.assertTrue(self.new_trip.is_approved)

    def test_cancel_trip(self):
        self.assertFalse(self.new_trip.is_cancelled)
        # Random member cannot cancel trip
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_cancelled(self.member)
        # Organiser cannot open trip before its public
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_cancelled(self.trip_organiser)
        self.new_trip.set_approved(self.do)
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_cancelled(self.trip_organiser)

        # With public
        self.new_trip.set_open(self.do)
        self.new_trip.set_cancelled(self.trip_organiser)
        self.new_trip.set_closed(self.do)
        self.new_trip.set_cancelled(self.trip_organiser)
        self.new_trip.refresh_from_db()
        self.assertTrue(self.new_trip.is_cancelled)

    def test_open_trip(self):
        self.assertFalse(self.new_trip.is_open)
        # Random member cannot open trip
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_open(self.member)
        # Organiser cannot open trip before its approved
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_open(self.trip_organiser)

        # With approval they can
        self.new_trip.set_approved(self.do)
        self.new_trip.set_open(self.trip_organiser)
        self.new_trip.refresh_from_db()
        self.assertTrue(self.new_trip.is_open)

    def test_close_trip(self):
        self.assertFalse(self.new_trip.is_closed)
        # Random member cannot close trip
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_closed(self.member)
        # Organiser cannot open trip before its approved
        with self.assertRaises(PermissionDenied):
            self.new_trip.set_closed(self.trip_organiser)

        # With approval they can
        self.new_trip.set_approved(self.do)
        self.new_trip.set_closed(self.trip_organiser)
        self.new_trip.refresh_from_db()
        self.assertTrue(self.new_trip.is_closed)
