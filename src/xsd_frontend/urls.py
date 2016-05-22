from django.conf.urls import patterns, include, url
from django.conf import settings

from views import *

urlpatterns = patterns('',
    url(r'^$', 'xsd_frontend.views.dashboard', name='dashboard'),
    url(r'^activity/$', ActivityTable.as_view(), name='activity_table'),
    #url(r'^activity/feed/$', ActivityFeed.as_view(), name='activity_feed'),
)
