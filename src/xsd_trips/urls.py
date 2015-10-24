from django.conf.urls import patterns, include, url
from django.conf import settings

from views import *

urlpatterns = patterns('',
      url(r'^$', TripList.as_view(), name='TripList'),
        url(r'^new/$', TripCreate.as_view(), name='TripCreate'),
)
