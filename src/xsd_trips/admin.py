from django.contrib import admin
from xsd_trips.models import Trip

class TripAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trip, TripAdmin)
