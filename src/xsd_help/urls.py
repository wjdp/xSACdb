from __future__ import unicode_literals

from django.conf.urls import url

from xsd_help.views import *

urlpatterns = [
    url(r'^(?P<page>.*)/$', HelpView.as_view(), name='HelpView'),
    url(r'^$', HelpView.as_view(), name='HelpView'),
]
