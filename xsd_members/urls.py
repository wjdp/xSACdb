from django.conf.urls import patterns, include, url
from django.conf import settings

from views import *

urlpatterns = patterns('',
	    url(r'^$', 'xsd_members.views.admin', name='members_admin'),
	    url(r'^search/$', MemberSearch.as_view(), name='MemberSearch'),
	    url(r'^list/$', MemberList.as_view(), name='MemberList'),
)