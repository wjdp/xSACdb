from django.conf.urls import patterns, include, url
from django.conf import settings

from django.views.generic.base import TemplateView

from views import *

urlpatterns = patterns('',
        url(r'^$', AboutView.as_view(), name='AboutView'),
        url(r'^database-officers/$', DatabaseOfficersView.as_view(), name='DatabaseOfficers'),

        url(r'all-update-requests/$', TemplateView.as_view(template_name='about_not_yet_implemented.html'), name='AllUpdateRequests'),
        url(r'assign-roles/$', TemplateView.as_view(template_name='about_not_yet_implemented.html'), name='AssignRoles'),
        url(r'application-tools/$', TemplateView.as_view(template_name='about_not_yet_implemented.html'), name='ApplicationTools'),
        url(r'django-admin/$', TemplateView.as_view(template_name='django_admin_warning.html'), name='DjangoAdminWarning'),

)
