from django.conf.urls import patterns, include, url
from django.conf import settings

from views import *

urlpatterns = patterns('',
	    url(r'^$', SitesOverview.as_view(), name='SitesOverview'),
	    url(r'^search/$', SitesSearch.as_view(), name='SitesSearch'),
)
