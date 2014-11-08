from django.conf.urls import patterns, include, url
from django.conf import settings

from xsd_help.views import *

urlpatterns = patterns('',
    url(r'^(?P<page>.*)/$', HelpView.as_view(), name='HelpView'),
    url(r'^$', HelpView.as_view(), name='HelpView'),
)
