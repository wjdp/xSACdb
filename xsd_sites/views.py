from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy


from models import *

class SitesOverview(ListView):
    model=Site
    template_name='sites_overview.html'
    context_object_name='sites'

class SitesSearch(ListView):
    model=Site
    template_name="sites_overview.html"
    context_object_name='sites'

class SiteCreate(CreateView):
    model=Site
    template_name="sites_update.html"
    context_object_name='sites'
    page_title='Add a Site'

    def get_context_data(self, **kwargs):
        context = super(SiteCreate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class SitesList(ListView):
    model=Site
    template_name="sites_list.html"
    context_object_name='sites'
    page_title='Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SitesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class SiteUpdate(UpdateView):
    model=Site
    template_name="sites_update.html"
    context_object_name='sites'
    success_url=reverse_lazy('SitesList')

    page_title='Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SiteUpdate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

def sitedetail_json(request,pk):
    site=get_object_or_404(Site, pk=pk)
    json_site=serializers.serialize("json",[site, ])
    return HttpResponse(json_site, mimetype='application/json')