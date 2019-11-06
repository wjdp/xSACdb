

from django.db import models
from django.conf import settings

AREA_CHOICES = (
    ('mem', 'Membership Details and Renewal'),
    ('tra', 'Training Records'),
    ('sit', 'Dive Sites'),
    ('tri', 'Trips'),
)


class UpdateRequest(models.Model):
    area=models.CharField(choices=AREA_CHOICES, max_length=3)
    lesson=models.ForeignKey('xsd_training.Lesson', blank=True, null=True, on_delete=models.PROTECT)
    site=models.ForeignKey('xsd_sites.Site', blank=True, null=True, on_delete=models.SET_NULL)
    request_body=models.TextField()
    response_body=models.TextField(blank=True)
    request_made_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_made_by', blank=True, null=True,
                                      on_delete=models.SET_NULL)
    response_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='response_by', blank=True, null=True,
                                  on_delete=models.SET_NULL)
    completed=models.BooleanField(default=False, verbose_name='Mark this issue as fixed')
    sent=models.DateTimeField(auto_now_add=True)
