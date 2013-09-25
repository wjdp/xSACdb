from django.views.generic.list import ListView

from models import *

class TripList(ListView):
	model=Trip
	template_name='trips_list.html'
	context_object_name='trips'