from django.db import models

class Trip(models.Model):
	name=models.CharField(max_length=50)
	date_from=models.DateField()
	date_to=models.DateField()
	trip_organiser=models.ForeignKey('auth.User')
	location=models.CharField(max_length=100)
	cost=models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
	notes=models.TextField(blank=True)
	max_depth=models.PositiveIntegerField(blank=True, null=True)
	min_qual=models.ForeignKey('xsd_training.Qualification')

	spaces=models.PositiveIntegerField(blank=True, null=True)
	accepting_signups=models.BooleanField(default=True)

class TripAttendee(models.Model):
	trip=models.ForeignKey('xsd_trips.Trip')
	attendee=models.ForeignKey('auth.User')
	accepted=models.BooleanField(default=False)
	deposit_paid=models.BooleanField(default=False)
	cost_paid=models.BooleanField(default=False)

	notes=models.TextField(blank=True)

	
