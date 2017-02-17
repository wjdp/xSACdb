from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireVerified

from models import Trip

class TripListUpcoming(RequireVerified, ListView):
    model=Trip
    template_name='xsd_trips/list.html'
    context_object_name='trips'
    queryset = Trip.objects.upcoming()

class TripListArchive(RequireVerified, ListView):
    model=Trip
    template_name='xsd_trips/list.html'
    context_object_name='trips'
    queryset = Trip.objects.past()

class TripCreate(RequireVerified, CreateView):
  model = Trip
  template_name = 'xsd_trips/create.html'

class TripDetail(RequireVerified, DetailView):
  model = Trip
  template_name = 'xsd_trips/detail.html'
