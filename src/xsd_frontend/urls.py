from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.templatetags.staticfiles import static

from views import *

favicon_view = RedirectView.as_view(url=static('icons/favicon.ico'), permanent=True)

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    url(r'^accounts/login/$', PreauthLoginView.as_view(), name='login'),
    url(r'^accounts/register/$', PreauthRegisterView.as_view(), name='register'),
    url(r'^accounts/logout/$', 'xsd_frontend.views.logout', name='logout'),

    url(r'^favicon\.ico$', favicon_view),
    url(r'manifest\.json$', TemplateView.as_view(
            template_name='browser/manifest.json',
            content_type='application/json'),
        name='app-manifest'
    ),
    url(r'browserconfig\.xml', TemplateView.as_view(
            template_name='browser/browserconfig.xml',
            content_type='application/xml'),
        name='app-browserconfig'
    ),

    url(r'service-worker\.js$', TemplateView.as_view(
            template_name='service-worker.js',
            content_type='text/javascript'),
        name='app-service-worker'),
)
