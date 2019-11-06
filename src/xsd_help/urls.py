

from django.conf.urls import url

from xsd_help.views import *

app_name = 'xsd_help'

urlpatterns = [
    url(r'^(?P<page>.*)/$', HelpView.as_view(), name='HelpView'),
    url(r'^$', HelpView.as_view(), name='HelpView'),
]
