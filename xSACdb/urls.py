from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

handler403='xsd_frontend.views.error403'

urlpatterns = patterns('',
    url(r'^$', 'xsd_frontend.views.dashboard', name='dashboard'),

    url(r'^accounts/login/$', 'xsd_frontend.views.login', name='login'),
    url(r'^accounts/logout/$', 'xsd_frontend.views.logout', name='logout'),
    
    url(r'^facebook/', include('django_facebook.urls')),

    url(r'^profile/$', 'xsd_members.views.view_my_profile', name='my-profile'),

    url(r'^members/', include('xsd_members.urls')),

    url(r'^training/', include('xsd_training.urls')),

    url(r'^sites/', include('xsd_sites.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
