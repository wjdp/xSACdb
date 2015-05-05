from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireVerified

from models import *

class TripList(RequireVerified, ListView):
	model=Trip
	template_name='trips_list.html'
	context_object_name='trips'

class TripCreate(RequireVerified, CreateView):
  model = Trip
  template_name = 'trips_create.html'
