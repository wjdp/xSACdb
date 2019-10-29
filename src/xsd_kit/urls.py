

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='kit_overview.html'), name='KitOverview'),
    url(r'^club/$', ClubKitListView.as_view(), name='KitClubKit'),
]
