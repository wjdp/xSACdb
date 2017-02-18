from __future__ import unicode_literals

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

    def state_class(self):
        return 'trip-state-{}'.format(self.STATE_CLASS_MAP[self.state])
