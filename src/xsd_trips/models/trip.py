from __future__ import unicode_literals

from django.db import models

from xsd_members.models import MemberProfile

from .fake import TripFakeDataMixin
from .trip_manager import TripManager
from .trip_member import TripMember


class Trip(models.Model, TripFakeDataMixin):
    """Representation of a trip"""

    objects = TripManager()

    owner = models.ForeignKey(MemberProfile, related_name='trip_owner')

    NAME_HELP_TEXT = 'Friendly name.'
    name = models.CharField(max_length=64, help_text=NAME_HELP_TEXT)

    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    COST_HELP_TEXT = 'Advertised cost of trip.'
    cost = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True, help_text=COST_HELP_TEXT)

    SPACES_HELP_TEXT = 'Number of spaces to advertise.'
    spaces = models.PositiveIntegerField(blank=True, null=True, help_text=SPACES_HELP_TEXT)

    DESCRIPTION_HELP_TEXT = 'Viewable by all members.'
    description = models.TextField(blank=True, help_text=DESCRIPTION_HELP_TEXT)

    MAX_DEPTH_HELP_TEXT = 'Indication of the maximum planned depth of dives.'
    max_depth = models.PositiveIntegerField(blank=True, null=True, help_text=MAX_DEPTH_HELP_TEXT)
    MIN_QUAL_HELP_TEXT = 'Indication of the minimum qualification needed to participate on this trip\'s diving.'
    min_qual = models.ForeignKey('xsd_training.Qualification', blank=True, null=True, help_text=MIN_QUAL_HELP_TEXT)

    STATES = (
        (10, 'Cancelled'),
        (20, 'New'),
        (30, 'Pending'),
        (40, 'Approved'),
        (50, 'Accepting sign-ups'),
        (80, 'Closed'),
        (99, 'Completed'),
    )
    state = models.IntegerField(choices=STATES, default=20)

    members = models.ManyToManyField('xsd_members.MemberProfile', blank=True, through=TripMember,
                                     related_name='trip_members')

    def __unicode__(self):
        return '{}'.format(self.name)
