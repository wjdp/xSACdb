from django.db import models
from django.conf import settings

class Trip(models.Model):
	name=models.CharField(max_length=50)
	date_from=models.DateField()
	date_to=models.DateField()
	trip_organiser=models.ForeignKey(settings.AUTH_USER_MODEL)
	location=models.CharField(max_length=100)
	cost=models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
	notes=models.TextField(blank=True)
	max_depth=models.PositiveIntegerField(blank=True, null=True)
	min_qual=models.ForeignKey('xsd_training.Qualification')

	sites=models.ManyToManyField('xsd_sites.Site', blank=True)

	spaces=models.PositiveIntegerField(blank=True, null=True)
	accepting_signups=models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

class TripAttendee(models.Model):
	trip=models.ForeignKey('xsd_trips.Trip')
	attendee=models.ForeignKey(settings.AUTH_USER_MODEL)
	accepted=models.BooleanField(default=False)
	deposit_paid=models.BooleanField(default=False)
	cost_paid=models.BooleanField(default=False)

	notes=models.TextField(blank=True)

	def __unicode__(self):
		return self.attendee.username + " on " + self.trip.name


