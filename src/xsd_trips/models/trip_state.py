from __future__ import unicode_literals

from actstream import action
from django.core.exceptions import PermissionDenied
from reversion import revisions
from django.db import transaction

STATE_DENIED = 10  # Created then denied
STATE_NEW = 20  # Brand new and awaiting approval
STATE_APPROVED = 40  # Approved and awaiting opening

STATE_CANCELLED = 45  # Having been opened, now closed
STATE_OPEN = 50  # Open for viewing
STATE_CLOSED = 80  # Closed for sign-ups
STATE_COMPLETED = 90  # Trip done


class TripStateMixin(object):
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
        return self.state >= STATE_APPROVED

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

    # Methods that do things...

    def set_denied(self, actor):
        if not self.can_deny(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_DENIED
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip request denied')
            action.send(actor, verb='denied trip request', target=self, state=STATE_DENIED, style='trip-denied')

    def set_approved(self, actor):
        if not self.can_approve(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_APPROVED
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip request approved')
            action.send(actor, verb='approved trip request', target=self, state=STATE_APPROVED, style='trip-approved')

    def set_cancelled(self, actor):
        if not self.can_cancel(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_CANCELLED
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip cancelled')
            action.send(actor, verb='cancelled trip', target=self, state=STATE_CANCELLED, style='trip-cancelled')

    def set_open(self, actor):
        if not self.can_open(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_OPEN
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip opened')
            action.send(actor, verb='opened trip', target=self, state=STATE_OPEN, style='trip-opened')


    def set_closed(self, actor):
        if not self.can_close(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_CLOSED
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip closed')
            action.send(actor, verb='closed trip', target=self, state=STATE_CLOSED, style='trip-closed')


    def set_completed(self, actor):
        if not self.can_complete(actor):
            raise PermissionDenied
        with transaction.atomic(), revisions.create_revision():
            self.state = STATE_COMPLETED
            self.save()
            revisions.set_user(actor)
            revisions.set_comment('Trip completed')
            action.send(actor, verb='completed trip', target=self, state=STATE_CLOSED, style='trip-completed')

