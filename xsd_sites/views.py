from django.views.generic.list import ListView
from models import *

class SitesOverview(ListView):
	model=Site
	template_name='sites_overview.html'
	context_object_name='sites'

class SitesSearch(ListView):
	model=Site
	template_name="sites_overview.html"
	context_object_name='sites'
