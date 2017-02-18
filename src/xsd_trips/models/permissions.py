from __future__ import unicode_literals

from xSACdb.roles.functions import *

from .states import *

class TripPermissionMixin(object):
    def _is_modifier(self, user):
        return is_trips(user) or self.owner == user.get_profile()

    def can_view(self, user):
        if self.is_public:
            return is_verified(user)
        else:
            return self._is_modifier(user)

    def can_create(self, user):
        return is_verified(user)

    def can_edit(self, user):
        if self.state in (STATE_DENIED, STATE_CLOSED, STATE_CANCELLED):
            return False
        return self._is_modifier(user)

    def can_deny(self, user):
        if self.state in (STATE_NEW, ):
            return is_trips(user)

    def can_approve(self, user):
        if self.state in (STATE_DENIED, STATE_NEW):
            return is_trips(user)

    def can_delete(self, user):
        # Can only delete before public
        if not self.is_public:
            return self._is_modifier(user)
        else:
            return False

    def can_cancel(self, user):
        if self.state != STATE_DENIED:
            return self._is_modifier(user)
        else:
            return False

    def can_open(self, user):
        if self.state in (STATE_APPROVED, STATE_CANCELLED, STATE_CLOSED):
            return self._is_modifier(user)
        else:
            return False

    def can_close(self, user):
        if self.state in (STATE_APPROVED, STATE_CANCELLED, STATE_OPEN):
            return self._is_modifier(user)
        else:
            return False

    def can_complete(self, user):
        if self.state in (STATE_OPEN, STATE_CLOSED):
            return self._is_modifier(user)
        else:
            return False
