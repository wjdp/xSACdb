

import reversion
from django.conf import settings
from django.core.exceptions import PermissionDenied
from reversion import revisions

from xsd_frontend.activity import DoAction

STATE_DENIED = 10  # Created then denied
STATE_NEW = 20  # Brand new and awaiting approval
STATE_APPROVED = 40  # Approved and awaiting opening

STATE_CANCELLED = 45  # Having been opened, now closed
STATE_OPEN = 50  # Open for viewing
STATE_CLOSED = 80  # Closed for sign-ups
STATE_COMPLETED = 90  # Trip done


class TripStateMixin:
    @property
    def is_denied(self):
        return self.state == STATE_DENIED

    @property
    def is_new(self):
        return self.state == STATE_NEW

    @property
    def is_approved(self):
        return self.state == STATE_APPROVED

    @property
    def is_public(self):
        return self.state >= STATE_CANCELLED

    @property
    def is_cancelled(self):
        return self.state == STATE_CANCELLED

    @property
    def is_open(self):
        return self.state == STATE_OPEN

    @property
    def is_closed(self):
        return self.state == STATE_CLOSED

    @property
    def is_completed(self):
        return self.state >= STATE_COMPLETED

    STATE_CLASS_MAP = {
        STATE_DENIED: 'denied',
        STATE_NEW: 'new',
        STATE_APPROVED: 'approved',
        STATE_CANCELLED: 'cancelled',
        STATE_OPEN: 'open',
        STATE_CLOSED: 'closed',
        STATE_COMPLETED: 'completed',
    }

    @property
    def state_class(self):
        return 'trip-state-{}'.format(self.STATE_CLASS_MAP[self.state])

    STATE_OWNER_HELP_TEXT = {
        STATE_DENIED: settings.CLUB['trip_owner_denied'],
        STATE_NEW: settings.CLUB['trip_owner_new'],
        STATE_APPROVED: settings.CLUB['trip_owner_approved'],
        STATE_CANCELLED: settings.CLUB['trip_owner_cancelled'],
        STATE_OPEN: settings.CLUB['trip_owner_open'],
        STATE_CLOSED: settings.CLUB['trip_owner_closed'],
        STATE_COMPLETED: settings.CLUB['trip_owner_completed'],
    }

    @property
    def owner_help_text(self):
        return self.STATE_OWNER_HELP_TEXT[self.state]

    STATE_OFFICER_HELP_TEXT = {
        STATE_DENIED: settings.CLUB['trip_officer_denied'],
        STATE_NEW: settings.CLUB['trip_officer_new'],
        STATE_APPROVED: settings.CLUB['trip_officer_approved'],
        STATE_CANCELLED: settings.CLUB['trip_officer_cancelled'],
        STATE_OPEN: settings.CLUB['trip_officer_open'],
        STATE_CLOSED: settings.CLUB['trip_officer_closed'],
        STATE_COMPLETED: settings.CLUB['trip_officer_completed'],
    }

    @property
    def officer_help_text(self):
        return self.STATE_OFFICER_HELP_TEXT[self.state]

    # Methods that do things...

    def set_denied(self, actor):
        if not self.can_deny(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_DENIED
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='denied trip request', target=self, state=STATE_DENIED, style='trip-denied')

    def set_approved(self, actor):
        if not self.can_approve(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_APPROVED
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='approved trip request', target=self, state=STATE_APPROVED,
                        style='trip-approved')

    def set_cancelled(self, actor):
        if not self.can_cancel(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_CANCELLED
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='cancelled trip', target=self, state=STATE_CANCELLED, style='trip-cancelled')

    def set_open(self, actor):
        if not self.can_open(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_OPEN
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='opened trip', target=self, state=STATE_OPEN, style='trip-opened')

    def set_closed(self, actor):
        if not self.can_close(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_CLOSED
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='closed trip', target=self, state=STATE_CLOSED, style='trip-closed')

    def set_completed(self, actor):
        if not self.can_complete(actor):
            raise PermissionDenied
        with DoAction() as action, reversion.create_revision():
            self.state = STATE_COMPLETED
            self.save()
            revisions.set_user(actor)
            action.set(actor=actor, verb='completed trip', target=self, state=STATE_CLOSED, style='trip-completed')
