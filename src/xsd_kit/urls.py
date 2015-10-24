from django.conf.urls import patterns, include, url
from django.conf import settings

from django.views.generic.base import TemplateView

from views import *

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='kit_overview.html'), name='KitOverview'),
    url(r'^club/$', ClubKitListView.as_view(), name='KitClubKit'),
)
