from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireVerified, RequireTripsOfficer
from xSACdb.roles.functions import is_trips

from models import Trip


class TripListUpcoming(RequireVerified, ListView):
    """Current & future trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        if is_trips(self.request.user):
            return Trip.objects.upcoming_all()
        else:
            return Trip.objects.upcoming()


class TripListArchive(RequireVerified, ListView):
    """Past trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'
    queryset = Trip.objects.past()


class TripListMine(RequireVerified, ListView):
    """Admin view of denied, new and approved trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return super(TripListMine, self).get_queryset().filter(owner=self.request.user.get_profile()).order_by('-date_start')


class TripListAdmin(RequireTripsOfficer, ListView):
    """Admin view of denied, new and approved trips"""
    model = Trip
    template_name = 'xsd_trips/list.html'
    context_object_name = 'trips'
    queryset = Trip.objects.private()


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
        # Patch in setting the trip owner
        trip = form.save(commit=False)
        trip.owner = self.request.user.get_profile()
        trip.save()
        return super(TripCreate, self).form_valid(form)


class TripDetail(RequireVerified, DetailView):
    model = Trip
    template_name = 'xsd_trips/detail.html'

    def get_queryset(self):
        return super(TripDetail, self).get_queryset().select_related()


class TripUpdate(RequireVerified, UpdateView):
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

    def get_queryset(self):
        return super(TripUpdate, self).get_queryset().select_related()
