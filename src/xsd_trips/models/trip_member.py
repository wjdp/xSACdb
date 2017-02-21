from __future__ import unicode_literals

import reversion
from actstream import action
from actstream import actions
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db import transaction
from django.utils.functional import cached_property


class TripMember(models.Model):
    trip = models.ForeignKey('xsd_trips.Trip', on_delete=models.CASCADE)
    member = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.CASCADE)

    STATE_INTERESTED = 10
    STATE_ACCEPTED = 20
    STATE_DEPOSIT_PAID = 30
    STATE_FULL_PAID = 40

    STATES = (
        # (STATE_INTERESTED, 'Interested'),
        (STATE_ACCEPTED, 'Accepted'),
        # (STATE_DEPOSIT_PAID, 'Deposit Paid'),
        # (STATE_FULL_PAID, 'Full Paid'),
    )

    state = models.IntegerField(choices=STATES, default=STATE_ACCEPTED)

    @cached_property
    def qualification_issue(self):
        """Is there a mismatch between the member's qualification and the trip"""
        if self.trip.min_qual == None:
            # No qual needed
            return False
        if self.member.top_qual() == None:
            # Has no qual
            return True
        return self.member.top_qual().rank < self.trip.min_qual.rank


class TripMemberMixin(object):
    @cached_property
    def spaces_taken(self):
        return TripMember.objects.filter(trip=self, state__gte=TripMember.STATE_ACCEPTED).count()

    @cached_property
    def spaces_left(self):
        return max(0, self.spaces - self.spaces_taken)

    @cached_property
    def spaces_over(self):
        return max(0, self.spaces_taken - self.spaces)

    @cached_property
    def spaces_list(self):
        """Returns a list of spaces and their states. Used to visualise trip members."""
        if self.spaces:
            # Restricted spaces
            sl = []
            for i in range(0, self.spaces):
                if i < self.spaces_taken:
                    sl.append('taken')
                else:
                    sl.append('empty')
            return sl
        else:
            return ['undef'] * self.spaces_taken

    def add_members(self, members, actor):
        """Add a list of members to trip"""
        if not self.can_add(actor):
            raise PermissionDenied
        # Currently we're not doing anything with member 'state' so we set that here to full approval.
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Adding attendees')
            trip_members = TripMember.objects.filter(trip=self)
            for member in members:
                if member in trip_members:
                    # Ensure we do not duplicate attendees
                    continue
                # Add relationship
                TripMember.objects.create(
                    trip=self,
                    member=member,
                    state=TripMember.STATE_ACCEPTED,
                )
                # Newly added member should follow trip
                actions.follow(member.user, self)
                # Send action
                action.send(actor, verb='added', action_object=member, target=self, style='trip-attendee-add')

    def remove_members(self, members, actor):
        """Remove a list of members from a trip"""
        if not self.can_remove(actor):
            raise PermissionDenied
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Removing attendees')
            for member in members:
                tm = TripMember.objects.filter(trip=self, member=member)
                tm.delete()
                action.send(actor, verb='removed', action_object=member, target=self, style='trip-attendee-remove')
