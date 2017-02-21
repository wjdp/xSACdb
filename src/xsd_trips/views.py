from __future__ import unicode_literals

import csv

import datetime
import reversion
from actstream import action
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ViewDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireVerified, RequirePermission, RequireTripsOfficer
from xSACdb.roles.functions import is_trips

from models import Trip
from xSACdb.views import ActionView
from xsd_frontend.versioning import VersionHistoryView
from xsd_members.bulk_select import get_bulk_members
from xsd_members.models import MemberProfile
from xsd_trips.models.trip_member import TripMember


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
        context['attendees'] = TripMember.objects.filter(trip=self.object)
        # To populate warning dialogue
        context['export_csv_columns'] = TripAttendeeRosterDump.COLUMNS
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


class TripSet(RequireVerified, ActionView):
    model = Trip

    def deny(self, request):
        self.get_object().set_denied(request.user)

    def approve(self, request):
        self.get_object().set_approved(request.user)

    def cancel(self, request):
        self.get_object().set_cancelled(request.user)

    def open(self, request):
        self.get_object().set_open(request.user)

    def close(self, request):
        self.get_object().set_closed(request.user)

    def complete(self, request):
        self.get_object().set_completed(request.user)

    def add(self, request):
        members = get_bulk_members(request)
        self.get_object().add_members(members=members, actor=self.request.user)
        messages.add_message(self.request, messages.SUCCESS,
                             'Added {} members to {}'.format(len(members), self.get_object()))

    def remove(self, request):
        members = [MemberProfile.objects.get(pk=request.POST['pk'])]
        self.get_object().remove_members(members=members, actor=self.request.user)
        messages.add_message(self.request, messages.SUCCESS,
                             'Removed {} member from {}'.format(len(members), self.get_object()))


class TripDelete(RequirePermission, DeleteView):
    model = Trip
    permission = 'can_delete'
    template_name = 'base/delete.html'
    success_url = reverse_lazy('xsd_trips:TripListUpcoming')

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             settings.CLUB['trip_delete_success'].format(self.get_object().name))
        return super(TripDelete, self).delete(request, *args, **kwargs)

class TripAttendeeRosterDump(View):
    model = TripMember

    COLUMNS = (
        ('name', 'full_name'),
        ('gender', 'gender'),
        ('date_of_birth', 'date_of_birth'),
        ('address', 'address'),
        ('postcode', 'postcode'),
        ('home_phone', 'home_phone'),
        ('mobile_phone', 'mobile_phone'),
        ('email', 'email'),
        ('next_of_kin_name', 'next_of_kin_name'),
        ('next_of_kin_relation', 'next_of_kin_relation'),
        ('next_of_kin_phone', 'next_of_kin_phone'),
    )

    @cached_property
    def trip(self):
        return Trip.objects.get(pk=self.kwargs['pk'])


    def get_queryset(self):
        return self.model.objects.filter(trip=self.trip)

    def get_filename(self):
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return '{}_{}_roster.csv'.format(now, slugify(self.trip.name))

    # We use post so 99% of users have to use our form with a data protection notice.
    def post(self, request, *args, **kwargs):
        # Security
        if not self.trip.can_view_attendee_details(request.user):
            raise PermissionDenied

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.get_filename())

        writer = csv.writer(response)

        writer.writerow([header[0] for header in self.COLUMNS])
        for attendee in self.get_queryset():
            writer.writerow([getattr(attendee.member, column[1]) for column in self.COLUMNS])
        return response
