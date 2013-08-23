from django.views.generic.list import ListView
from models import *

class SitesOverview(ListView):
	model=Site
	template_name="sites_overview.html"

class SitesSearch(ListView):
	model=Site
	template_name="sites_overview.html"