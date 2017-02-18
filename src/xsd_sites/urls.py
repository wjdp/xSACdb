from django.conf.urls import patterns, url

from views import *
from models import Site
from xsd_frontend.versioning import VersionHistoryView

urlpatterns = patterns('',
    url(r'^$', SitesOverview.as_view(), name='SitesOverview'),
    url(r'^search/$', SitesSearch.as_view(), name='SitesSearch'),
    url(r'^add/$', SiteCreate.as_view(), name='SiteCreate'),
    url(r'^edit/$', SitesList.as_view(), name='SitesList'),
    url(r'^edit/(?P<pk>\d+)/$', SiteUpdate.as_view(), name='SiteUpdate'),
    url(r'^edit/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='SiteHistory',
       kwargs={'model': Site}),

    url(r'^json/(?P<pk>\d+)/$', 'xsd_sites.views.sitedetail_json', name='sitedetail_json'),
)
