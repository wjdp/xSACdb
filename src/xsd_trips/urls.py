from __future__ import unicode_literals

from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', TripListUpcoming.as_view(), name='TripListUpcoming'),
    url(r'^archive/$', TripListArchive.as_view(), name='TripListArchive'),
    url(r'^my/$', TripListMine.as_view(), name='TripListMine'),
    url(r'^admin/$', TripListAdmin.as_view(), name='TripListAdmin'),

    url(r'^new/$', TripCreate.as_view(), name='TripCreate'),

    url(r'^(?P<pk>\d+)/$', TripDetail.as_view(), name='TripDetail'),
    url(r'^(?P<pk>\d+)/edit/$', TripUpdate.as_view(), name='TripUpdate'),
    url(r'^(?P<pk>\d+)/history/$', TripHistory.as_view(), name='TripHistory'),
    url(r'^(?P<pk>\d+)/action/(?P<action>\w+)/$', TripSet.as_view(), name='TripSet'),
    url(r'^(?P<pk>\d+)/delete/$', TripDelete.as_view(), name='TripDelete'),
    url(r'^(?P<pk>\d+)/roster/$', TripAttendeeRosterDump.as_view(), name='TripAttendeeRosterDump'),
]
