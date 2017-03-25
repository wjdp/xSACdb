from __future__ import unicode_literals

import reversion
from django.conf import settings
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from forms import SiteForm
from models import Site
from xSACdb.roles.decorators import require_verified
from xSACdb.roles.mixins import RequireSiteAdministrator, RequireVerified
from xsd_frontend.activity import DoAction


class SitesOverview(RequireVerified, ListView):
    model = Site
    template_name = 'sites_overview.html'
    context_object_name = 'sites'

    def get_context_data(self, **kwargs):
        c = super(SitesOverview, self).get_context_data(**kwargs)
        # Filter the sites returned to the view
        sites = self.get_queryset()
        sites_real = []
        for site in sites:
            if site.location:
                sites_real.append(site)
        c[self.context_object_name] = sites_real
        c['GEOPOSITION_GOOGLE_MAPS_API_KEY'] = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
        return c


class SitesSearch(RequireVerified, ListView):
    model = Site
    template_name = "sites_overview.html"
    context_object_name = 'sites'


class SiteCreate(RequireSiteAdministrator, CreateView):
    model = Site
    template_name = "sites_update.html"
    context_object_name = 'sites'
    page_title = 'Add a Site'
    success_url = reverse_lazy('xsd_sites:SitesList')
    form_class = SiteForm

    def get_context_data(self, **kwargs):
        context = super(SiteCreate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        with DoAction() as action, reversion.create_revision():
            site = form.save()
            action.set(actor=self.request.user, verb="created site", target=site, style='site-create')
            return super(SiteCreate, self).form_valid(form)


class SitesList(RequireSiteAdministrator, ListView):
    model = Site
    template_name = "sites_list.html"
    context_object_name = 'sites'
    page_title = 'Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SitesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class SiteUpdate(RequireSiteAdministrator, UpdateView):
    model = Site
    template_name = "sites_update.html"
    context_object_name = 'sites'
    success_url = reverse_lazy('xsd_sites:SitesList')
    form_class = SiteForm

    page_title = 'Edit a Site'

    def get_context_data(self, **kwargs):
        context = super(SiteUpdate, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        with DoAction() as action, reversion.create_revision():
            site = form.save()
            action.set(actor=self.request.user, verb="updated site", target=site, style='site-update')
            return super(SiteUpdate, self).form_valid(form)


@require_verified
def sitedetail_json(request, pk):
    site = get_object_or_404(Site, pk=pk)
    json_site = serializers.serialize("json", [site, ])
    return HttpResponse(json_site, mimetype='application/json')
