STATE_CANCELLED = 10
STATE_NEW = 20
STATE_PENDING = 30
STATE_APPROVED = 40
STATE_OPEN = 50
STATE_CLOSED = 80
STATE_COMPLETED = 90

class TripStateMixin(object):
    def awaiting_approval(self):
        return self.state == STATE_PENDING
