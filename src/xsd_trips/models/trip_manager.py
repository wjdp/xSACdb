from __future__ import unicode_literals

import datetime
from django.db import models

from .states import *


class TripManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(TripManager, self).all(*args, **kwargs).order_by('date_start')

    def upcoming(self):
        """Approved trips in the future"""
        return self.filter(state__gte=self.model.STATE_OPEN).filter(date_end__gte=datetime.date.today()).order_by('date_start')

    def past(self):
        """Approved trips in the future"""
        return self.filter(date_end__lte=datetime.date.today()).order_by('-date_start')

