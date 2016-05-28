from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import *

urlpatterns = patterns('',
    url(r'^$', 'xsd_frontend.views.dashboard', name='dashboard'),

    url(r'^accounts/login/$', PreauthLoginView.as_view(), name='login'),

    # url(r'^accounts/login/$', 'xsd_frontend.views.login', name='login'),
    url(r'^accounts/register/$', 'xsd_frontend.views.register', name='login'),
    url(r'^accounts/logout/$', 'xsd_frontend.views.logout', name='logout'),

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
