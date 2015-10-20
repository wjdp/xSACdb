from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy

from xSACdb.roles.decorators import require_site_administrator, require_verified
from xSACdb.roles.mixins import RequireSiteAdministrator, RequireVerified

from models import *
from forms import *

class SitesOverview(RequireVerified, ListView):
    model=Site
    template_name='sites_overview.html'
    context_object_name='sites'

class SitesSearch(RequireVerified, ListView):
    model=Site
    template_name="sites_overview.html"
    context_object_name='sites'

class SiteCreate(RequireSiteAdministrator, CreateView):
    model=Site
    template_name="sites_update.html"
    context_object_name='sites'
    page_title='Add a Site'
    success_url=reverse_lazy('SitesList')
    form_class = SiteForm

    def get_context_data(self, **kwargs):
        context = super(SiteCreate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class SitesList(RequireSiteAdministrator, ListView):
    model=Site
    template_name="sites_list.html"
    context_object_name='sites'
    page_title='Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SitesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class SiteUpdate(RequireSiteAdministrator, UpdateView):
    model=Site
    template_name="sites_update.html"
    context_object_name='sites'
    success_url=reverse_lazy('SitesList')
    form_class = SiteForm

    page_title='Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SiteUpdate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

@require_verified
def sitedetail_json(request,pk):
    site=get_object_or_404(Site, pk=pk)
    json_site=serializers.serialize("json",[site, ])
    return HttpResponse(json_site, mimetype='application/json')
