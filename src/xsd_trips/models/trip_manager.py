

import datetime
from django.db import models

from .trip_state import *


class TripManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(TripManager, self).all(*args, **kwargs).order_by('date_start')

    def upcoming_all(self):
        return self.filter(date_start__gte=datetime.date.today() - datetime.timedelta(days=14)).order_by('date_start')

    def upcoming(self):
        """Approved trips in the future"""
        return self.upcoming_all().filter(state__gte=self.model.STATE_CANCELLED)

    def private(self):
        """Admin view of denied, new and approved trips"""
        return self.filter(state__lte=self.model.STATE_APPROVED).order_by('date_start')

    def past(self):
        """Approved trips in the future"""
        return self.filter(date_end__lte=datetime.date.today()).order_by('-date_start')
