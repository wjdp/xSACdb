from __future__ import unicode_literals

import datetime
from actstream.actions import follow
from reversion import revisions as reversion
from django.core.urlresolvers import reverse
from django.db import models

from xsd_members.models import MemberProfile

from .trip_manager import TripManager
from .trip_member import TripMember, TripMemberMixin

from .trip_fake import TripFakeDataMixin
from .trip_permission import TripPermissionMixin
from .trip_state import *


@reversion.register()
class Trip(TripStateMixin,
           TripPermissionMixin,
           TripMemberMixin,
           TripFakeDataMixin,
           models.Model):
    """Representation of a trip"""

    objects = TripManager()

    owner = models.ForeignKey(MemberProfile, related_name='trip_owner', verbose_name='Organiser')

    name = models.CharField(max_length=64, help_text='Friendly name.')

    date_start = models.DateField(verbose_name='Departs', help_text='dd/mm/yyyy')
    date_end = models.DateField(blank=True, null=True, verbose_name='Returns', help_text='dd/mm/yyyy')

    cost = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True,
                               help_text='Advertised cost of trip.')

    spaces = models.PositiveIntegerField(blank=True, null=True, help_text='Number of spaces to advertise.')

    description = models.TextField(blank=True, help_text='Viewable by all members.')

    max_depth = models.PositiveIntegerField(blank=True, null=True, verbose_name='Maximum depth',
                                            help_text='Indication of the maximum planned depth of dives.')
    min_qual = models.ForeignKey('xsd_training.Qualification', blank=True, null=True,
                                 verbose_name='Minimum qualification',
                                 help_text='Indication of the minimum qualification needed to participate on this trip\'s diving.')

    # Copy states from states
    STATE_DENIED = STATE_DENIED
    STATE_NEW = STATE_NEW
    STATE_APPROVED = STATE_APPROVED

    STATE_CANCELLED = STATE_CANCELLED
    STATE_OPEN = STATE_OPEN
    STATE_CLOSED = STATE_CLOSED
    STATE_COMPLETED = STATE_COMPLETED

    STATES = (
        (STATE_DENIED, 'Denied'),
        (STATE_NEW, 'New'),
        (STATE_APPROVED, 'Approved'),
        (STATE_CANCELLED, 'Cancelled'),
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed'),
        (STATE_COMPLETED, 'Completed'),
    )

    state = models.IntegerField(choices=STATES, default=STATE_NEW)

    members = models.ManyToManyField('xsd_members.MemberProfile', blank=True, through=TripMember,
                                     related_name='trip_members')

    @property
    def uid(self):
        return "T{:0>4d}".format(self.pk)

    @property
    def date_final(self):
        """As date_end is optional this will match either that or date_start"""
        return self.date_end or self.date_start

    @property
    def in_past(self):
        return self.date_final < datetime.date.today()

    def get_absolute_url(self):
        return reverse('xsd_trips:TripDetail', kwargs={'pk': self.pk})

    def save(self, **kwargs):
        if not self.pk:
            # If new ensure the owner follows their trip
            super(Trip, self).save(**kwargs)
            follow(self.owner.user, self, actor_only=False)
        else:
            super(Trip, self).save(**kwargs)

    def __unicode__(self):
        return '{}'.format(self.name)
