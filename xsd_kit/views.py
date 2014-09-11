from django.shortcuts import render
from django.views.generic import ListView 

from xSACdb.roles.mixins import RequireVerified

from models import *

class ClubKitListView(RequireVerified, ListView):
	model = Kit
	template_name = 'kit_club_kit.html'
	context_object_name = 'kits'
	queryset = Kit.objects.filter(club_owned = True)

