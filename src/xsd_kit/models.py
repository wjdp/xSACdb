

from django.db import models
from django.conf import settings

TYPE_CHOICES = (
    ('WETS','Wetsuit'),
    ('SEMI','Semidry'),
    ('DRYS','Drysuit'),
    ('BCD','BCD'),
    ('WING','Wing'),
    ('REGS','Regs'),
    ('CYL','Cylinder'),
    ('MASK','Mask'),
    ('FINS','Fins'),
    ('SNRK','Snorkel'),
    ('COMP','Computer'),
    ('TORH','Torch'),
    ('SMB','SMB'),
    ('DSMB','DSMB'),
    ('REEL','Reel'),
)

class Kit(models.Model):
    club_id = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    size = models.CharField(max_length=64, blank=True)
    club_owned = models.BooleanField(blank=True, default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=9, blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=9, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    needs_testing = models.BooleanField(blank=True, default=False)
    test_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.club_id + ": " + self.name

    class Meta:
        verbose_name="Kit"
        verbose_name_plural="Bits of kit"
        ordering=['type', 'size', 'club_id']

class Loan(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    kit = models.ManyToManyField('Kit')
    approved = models.BooleanField(blank=True, default=False)
    notes = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
