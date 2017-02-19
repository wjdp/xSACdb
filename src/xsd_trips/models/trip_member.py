from __future__ import unicode_literals

from django.db import models


class TripMember(models.Model):
    trip = models.ForeignKey('xsd_trips.Trip', on_delete=models.CASCADE)
    member = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
