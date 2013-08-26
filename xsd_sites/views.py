from django.http import HttpResponse

from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers

from models import *

class SitesOverview(ListView):
	model=Site
	template_name='sites_overview.html'
	context_object_name='sites'

class SitesSearch(ListView):
	model=Site
	template_name="sites_overview.html"
	context_object_name='sites'

def sitedetail_json(request,pk):
	site=get_object_or_404(Site, pk=pk)
	json_site=serializers.serialize("json",[site, ])
	return HttpResponse(json_site, mimetype='application/json')