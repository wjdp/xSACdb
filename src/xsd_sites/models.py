from django.db import models
from geoposition.fields import GeopositionField

SITE_TYPES = [
    ('TR', 'Training Site'),
    ('IN', 'Inland Site'),
    ('OF', 'Offshore Site'),
]

class Site(models.Model):
    name=models.CharField(max_length=40)
    type=models.CharField(max_length=2, choices = SITE_TYPES)
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
