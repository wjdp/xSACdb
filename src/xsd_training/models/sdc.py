

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db import transaction
from reversion import revisions as reversion

SDC_TYPE_CHOICES = (
    ('clu', 'Club Diving'),
    ('saf', 'Safety and Rescue'),
    ('sea', 'Seamanship'),
    ('spe', 'Special Interest'),
    ('tec', 'Technical'),
)


class SDC(models.Model):
    title = models.CharField(max_length=50)
    min_qualification = models.ForeignKey('Qualification', blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(choices=SDC_TYPE_CHOICES, max_length=3)
    other_requirements = models.BooleanField(default=False)

    interested_members = models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)

    def __str__(self):
        return self.title

    def uid(self):
        return "PS{:0>4d}".format(self.pk)

    class Meta:
        verbose_name = "SDC"
        verbose_name_plural = "SDCs"
        ordering = ['title']


class SDCCategoryList:
    cat_id = ""
    cat_name = ""
    sdcs = []

    def __init__(self, cat_id, cat_name):
        self.cat_id = cat_id
        self.cat_name = cat_name


class SDCDisplay:
    sdc = None
    can_do = False


@reversion.register()
class PerformedSDC(models.Model):
    sdc = models.ForeignKey('SDC')
    datetime = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    trainees = models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)
    completed = models.BooleanField(default=False)

    # places = models.IntegerField()

    def add_trainees(self, trainees):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Added trainees')
            existing_trainees = self.trainees.all()
            for trainee in trainees:
                if trainee not in existing_trainees:
                    self.trainees.add(trainee)
            self.save()

    def remove_trainees(self, trainees):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Removed trainees')
            for trainee in trainees:
                self.trainees.remove(trainee)
            self.save()

    def __str__(self):
        if self.datetime:
            return "{} @ {}".format(self.sdc, self.datetime)
        else:
            return "{} @ TBD".format(self.sdc)

    def uid(self):
        return "PSDC{:0>4d}".format(self.pk)

    def get_absolute_url(self):
        return reverse('xsd_training:PerformedSDCDetail', kwargs={'pk': self.pk})
