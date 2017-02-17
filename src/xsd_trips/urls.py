from django.conf.urls import patterns, include, url
from django.conf import settings

from views import *

urlpatterns = patterns('',
    url(r'^$', TripListUpcoming.as_view(), name='TripListUpcoming'),
    url(r'^archive/$', TripListArchive.as_view(), name='TripListArchive'),

    url(r'^new/$', TripCreate.as_view(), name='TripCreate'),

    url(r'^(?P<pk>\d+)/$', TripDetail.as_view(), name='TripDetail'),

)
