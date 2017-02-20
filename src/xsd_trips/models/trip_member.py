from __future__ import unicode_literals

from django.db import models
from django.utils.functional import cached_property


class TripMember(models.Model):
    trip = models.ForeignKey('xsd_trips.Trip', on_delete=models.CASCADE)
    member = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)


class TripMemberMixin(object):
    @cached_property
    def spaces_taken(self):
        # TODO Implement
        return 5

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
