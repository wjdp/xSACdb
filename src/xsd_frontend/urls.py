from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import *

urlpatterns = patterns('',
    url(r'^$', 'xsd_frontend.views.dashboard', name='dashboard'),
    url(r'activity/$', ActivityTable.as_view(), name='activity_table'),
    #url(r'^activity/feed/$', ActivityFeed.as_view(), name='activity_feed'),

    url(r'manifest\.json$', TemplateView.as_view(
            template_name='manifest.json',
            content_type='application/json'),
        name='app-manifest'
    ),
    url(r'service-worker\.js$', TemplateView.as_view(
            template_name='service-worker.js',
            content_type='text/javascript'),
        name='app-manifest'),
)
