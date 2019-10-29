

from django.db import models
from reversion import revisions as reversion
from geoposition.fields import GeopositionField

SITE_TYPES = [
    ('TR', 'Training Site'),
    ('IN', 'Inland Site'),
    ('OF', 'Offshore Site'),
]

@reversion.register()
class Site(models.Model):
    name=models.CharField(max_length=128)
    type=models.CharField(max_length=8, choices = SITE_TYPES)
    address=models.TextField(blank=True)
    location=GeopositionField(blank=True, null=True)
    phone=models.CharField(max_length=20, blank=True)
    email=models.EmailField(blank=True)
    min_temp=models.IntegerField(blank=True, null=True)
    max_temp=models.IntegerField(blank=True, null=True)
    max_depth=models.IntegerField(blank=True, null=True)
    facilities=models.TextField(blank=True)

    def __str__(self):
        return self.name

    def uid(self):
        return "ST{:0>4d}".format(self.pk)

