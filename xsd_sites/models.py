from django.db import models
from geoposition.fields import GeopositionField

class Site(models.Model):
    name=models.CharField(max_length=40)
    address=models.TextField(blank=True)
    location=GeopositionField(blank=True, null=True)
    phone=models.CharField(max_length=20, blank=True)
    email=models.EmailField(blank=True)
    min_temp=models.IntegerField(blank=True, null=True)
    max_temp=models.IntegerField(blank=True, null=True)
    max_depth=models.IntegerField(blank=True, null=True)
    facilities=models.TextField(blank=True)

    def __unicode__(self):
        return self.name
