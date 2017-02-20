from django.db import models


class MembershipType(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
