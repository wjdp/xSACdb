from __future__ import unicode_literals

from xSACdb.roles.functions import *

from .trip_state import *


class TripPermissionMixin(object):
    def _is_modifier(self, user):
        return is_trips(user) or self.owner == user.get_profile()

    def can_view(self, user):
        if self.is_public:
            return is_verified(user)
        else:
            return self._is_modifier(user)

    def can_view_history(self, user):
        return self._is_modifier(user)

    def can_create(self, user):
        return is_verified(user)

    def can_edit(self, user):
        if self.state in (STATE_COMPLETED, ):
            return False
        return self._is_modifier(user)

    def can_deny(self, user):
        if self.state in (STATE_NEW,):
            return is_trips(user)

    def can_approve(self, user):
        if self.state in (STATE_DENIED, STATE_NEW):
            return is_trips(user)

    def can_delete(self, user):
        # Can only delete before public
        if self.is_public:
           return False
        else:
            return self._is_modifier(user)

    def can_cancel(self, user):
        if self.state not in (STATE_DENIED, STATE_NEW, STATE_APPROVED, STATE_CANCELLED, STATE_COMPLETED):
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
        # TODO only allow if trip in past
        if self.state in (STATE_OPEN, STATE_CLOSED):
            return self._is_modifier(user)
        else:
            return False

    def can_add(self, user):
        """Can add members to trip"""
        if self.state in (STATE_OPEN, STATE_CLOSED):
            return self._is_modifier(user)
        else:
            return False

    def can_remove(self, user):
        """Can remove members from trip"""
        return self.can_add(user)
