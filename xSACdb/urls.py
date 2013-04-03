from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xSACdb.views.home', name='home'),
    # url(r'^xSACdb/', include('xSACdb.foo.urls')),
    
    url(r'^$', 'xsd_frontend.views.dashboard', name='dashboard'),
    url(r'^login/$', 'xsd_frontend.views.login',),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
