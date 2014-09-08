from django.db import models

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
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    size = models.CharField(max_length=64, blank=True)
    club_owned = models.BooleanField(blank=True)
    owner = models.ForeignKey('auth.User', blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=9, blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=9, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name="Kit"
        verbose_name_plural="Kit"
        ordering=['type', 'size', 'name']

class Loan(models.Model):
    member = models.ForeignKey('auth.User')
    kit = models.ManyToManyField('Kit')
    approved = models.BooleanField(blank=True)
    notes = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
