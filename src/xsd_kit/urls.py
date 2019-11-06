

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import *

app_name = 'xsd_kit'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='kit_overview.html'), name='KitOverview'),
    url(r'^club/$', ClubKitListView.as_view(), name='KitClubKit'),
]
