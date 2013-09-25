from django.contrib import admin
from xsd_trips.models import *

class TripAdmin(admin.ModelAdmin):
    pass

class TripAttendeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trip, TripAdmin)
admin.site.register(TripAttendee, TripAttendeeAdmin)
