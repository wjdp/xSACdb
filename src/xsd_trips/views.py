from __future__ import unicode_literals

import reversion
from actstream import action
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ViewDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireVerified, RequirePermission, RequireTripsOfficer
from xSACdb.roles.functions import is_trips

from models import Trip
from xsd_frontend.versioning import VersionHistoryView


class TripListUpcoming(RequireVerified, ListView):
    """Current & future trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        if is_trips(self.request.user):
            return Trip.objects.upcoming_all().select_related()
        else:
            return Trip.objects.upcoming().select_related()


class TripListArchive(RequireVerified, ListView):
    """Past trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'
    queryset = Trip.objects.past().select_related()


class TripListMine(RequireVerified, ListView):
    """Admin view of denied, new and approved trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return super(TripListMine, self).get_queryset().filter(owner=self.request.user.get_profile()).order_by(
            '-date_start')


class TripListAdmin(RequireTripsOfficer, ListView):
    """Admin view of denied, new and approved trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'
    queryset = Trip.objects.private().select_related()


class TripCreate(RequireVerified, CreateView):
    model = Trip
    template_name = 'xsd_trips/edit.html'
    fields = (
        'name',
        'date_start',
        'date_end',
        'cost',
        'spaces',
        'max_depth',
        'min_qual',
        'description',
    )

    def form_valid(self, form):
        with reversion.create_revision() and transaction.atomic():
            reversion.set_comment('Create trip')
            # Patch in setting the trip owner
            trip = form.save(commit=False)
            # trip.owner = self.request.user.profile
            trip.owner = self.request.user.profile
            trip.save()
            action.send(self.request.user, verb='requested approval for trip', target=trip, style='trip-create')
            return super(TripCreate, self).form_valid(form)


class TripDetail(RequireVerified, RequirePermission, DetailView):
    model = Trip
    permission = 'can_view'
    template_name = 'xsd_trips/detail.html'

    def get_queryset(self):
        return super(TripDetail, self).get_queryset().select_related()

    def get_context_data(self, **kwargs):
        context = super(TripDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.object.name
        return context


class TripHistory(RequirePermission, VersionHistoryView):
    versioned_model = Trip
    permission = 'can_view_history'

    def get_permission_object(self):
        return Trip.objects.get(pk=self.kwargs['pk'])


class TripUpdate(RequireVerified, RequirePermission, UpdateView):
    model = Trip
    permission = 'can_edit'
    template_name = 'xsd_trips/edit.html'
    fields = (
        'name',
        'date_start',
        'date_end',
        'cost',
        'spaces',
        'max_depth',
        'min_qual',
        'description',
    )

    def get_queryset(self):
        return super(TripUpdate, self).get_queryset().select_related()

    def get_context_data(self, **kwargs):
        context = super(TripUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Edit Trip'
        return context

    def form_valid(self, form):
        with reversion.create_revision() and transaction.atomic():
            reversion.set_comment('Updated')
            action.send(self.request.user, verb='updated trip', target=self.get_object(), style='trip-update')
            return super(TripUpdate, self).form_valid(form)


class TripSet(RequireVerified, SingleObjectMixin, View):
    model = Trip

    def post(self, request, *args, **kwargs):
        func = getattr(self, self.kwargs['action'], None)
        if func:
            func(request)
            return redirect(self.get_object())
        else:
            raise ViewDoesNotExist('You ain\'t got a func in your trunk!')

    def deny(self, request):
        self.get_object().set_denied(request.user)

    def approve(self, request):
        self.get_object().set_approved(request.user)

    def cancel(self, request):
        self.get_object().set_cancelled(request.user)

    def open(self, request):
        self.get_object().set_open(request.user)
        return redirect(self.get_object())

    def close(self, request):
        self.get_object().set_closed(request.user)

    def complete(self, request):
        self.get_object().set_completed(request.user)


class TripDelete(RequirePermission, DeleteView):
    model = Trip
    permission = 'can_delete'
    template_name = 'base/delete.html'
    success_url = reverse_lazy('xsd_trips:TripListUpcoming')

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             settings.CLUB['trip_delete_success'].format(self.get_object().name))
        return super(TripDelete, self).delete(request, *args, **kwargs)
