from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from xsd_members.models import MemberProfile

from .trip_manager import TripManager
from .trip_member import TripMember

from .fake import TripFakeDataMixin
from .states import *


class Trip(models.Model, TripStateMixin, TripFakeDataMixin):
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

    # Copy states from states
    STATE_CANCELLED = STATE_CANCELLED
    STATE_NEW = STATE_NEW
    STATE_PENDING = STATE_PENDING
    STATE_APPROVED = STATE_APPROVED
    STATE_OPEN = STATE_OPEN
    STATE_CLOSED = STATE_CLOSED
    STATE_COMPLETED = STATE_COMPLETED

    STATES = (
        (STATE_CANCELLED, 'Cancelled'),
        (STATE_NEW, 'New'),
        (STATE_PENDING, 'Pending'),
        (STATE_APPROVED, 'Approved'),
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed'),
        (STATE_COMPLETED, 'Completed'),
    )

    state = models.IntegerField(choices=STATES, default=20)

    members = models.ManyToManyField('xsd_members.MemberProfile', blank=True, through=TripMember,
                                     related_name='trip_members')
    @property
    def uid(self):
        return "T{:0>4d}".format(self.pk)

    def get_absolute_url(self):
        return reverse('xsd_trips:TripDetail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return '{}'.format(self.name)
