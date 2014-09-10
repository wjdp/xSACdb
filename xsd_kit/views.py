from django.shortcuts import render
from django.views.generic import ListView 

from models import *

class ClubKitListView(ListView):
	model = Kit
	template_name = 'kit_club_kit.html'
	context_object_name = 'kits'
	queryset = Kit.objects.filter(club_owned = True)

