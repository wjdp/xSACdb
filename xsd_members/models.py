from django.db import models

from django_facebook.models import FacebookProfileModel

class MemberProfile(models.Model):
    user = models.OneToOneField('auth.User')
    gender = models.CharField(max_length=6, blank=True)
    fid = models.BigIntegerField(verbose_name=u'Facebook ID')
    token = models.CharField(max_length=150)


from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Make sure we create a MemberProfile when creating a User
def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)
