

from django.db import models
from django.db.models import Q
from reversion import revisions as reversion

from xsd_training.models import Lesson


class QualificationManager(models.Manager):
    def get_active(self, trainee=None):
        qs = Q(active=True)
        if trainee is not None:
            qs |= Q(performedqualification__trainee=trainee)
            qs |= Q(q_training_for=trainee)
            qs |= Q(lesson__performedlesson__trainee=trainee)
        return self.filter(qs).distinct()


class Qualification(models.Model):
    code = models.CharField(max_length=4, unique=True)
    title = models.CharField(max_length=50)
    rank = models.IntegerField()
    definition = models.TextField(blank=True)
    instructor_qualification = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = QualificationManager()

    def __unicode__(self): return self.title

    class Meta:
        ordering = ['rank']

    def lessons_by_mode(self, mode):
        """Return a QS of lessons for this qual given a mode"""
        lessons = Lesson.objects.filter(qualification=self, mode=mode)
        return lessons


@reversion.register()
class PerformedQualification(models.Model):
    MODE_CHOICES = (
        ('INT', 'Internal'),
        ('EXT', 'External'),
        ('XO', 'Crossover'),
        ('OTH', 'Other'),
    )

    trainee = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.CASCADE, editable=False)
    qualification = models.ForeignKey('xsd_training.Qualification', on_delete=models.PROTECT)
    mode = models.CharField(max_length=3, choices=MODE_CHOICES,
                            help_text="Internal: within this club, extenal: with another BSAC branch, crossover: from another agency.")
    xo_from = models.CharField(max_length=64, blank=True, null=True, verbose_name="Crossover From",
                               help_text="What qualification did the trainee crossover from?")

    signed_off_on = models.DateField(blank=True, null=True, help_text="Date when qualification was signed off in QRB.")
    signed_off_by = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.PROTECT, blank=True, null=True,
                                      related_name='pqs_signed', help_text="Who signed the QRB? Usually the branch DO.")

    # TODO: Add instructor_number here, migrate data from MemberProfiles

    notes = models.TextField(blank=True, null=True,
                             help_text="Both instructors and the trainee can see any notes written here.")

    created = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        ordering = ['qualification__rank']

    def uid(self):
        return "PQ{:0>4d}".format(self.pk)

    @property
    def mode_display(self):
        for mode in self.MODE_CHOICES:
            if mode[0] == self.mode:
                return mode[1]
        raise ValueError('Mode not in MODE_CHOICES')
