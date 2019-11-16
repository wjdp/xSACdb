

import datetime

from django.conf import settings
from django.core.cache import cache
from django.db import models, transaction
from django.urls import reverse
from reversion import revisions as reversion

from xSACdb.roles.functions import is_instructor, is_training
from xsd_auth.permissions import ModelPermissions, ModelComposeMixin


class LessonManager(models.Manager):
    def by_qualification_detailed(self, qualification):
        """Return a list of tuples (mode, lessons)"""

        def map_mode_to_lessons(mode):
            lessons_in_mode = self.filter(qualification=qualification, mode=mode[0])
            return (mode, lessons_in_mode)

        key = "by_qualification_detailed--{qualification}".format(qualification=qualification.code)
        val = cache.get(key)
        if val is None:
            val = list(map(map_mode_to_lessons, Lesson.MODE_CHOICES))
            val = [i for i in val if len(i[1]) > 0]  # Remove empty rows
            cache.set(key, val, 86400)
        return val


class Lesson(models.Model):
    MODE_CHOICES = (
        ('TH', 'Theory'),
        ('SW', 'Sheltered Water'),
        ('OW', 'Open Water'),
        ('DP', 'Dry Practical'),
        ('XP', 'Experience'),
        ('WS', 'Workshop'),
        ('PQ', 'Post Qualification'),
        ('XO', 'Cross-over'),
        ('AS', 'Assessment'),
    )
    qualification = models.ForeignKey('Qualification', on_delete=models.PROTECT)
    code = models.CharField(max_length=5, blank=True)
    title = models.CharField(max_length=90)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    max_depth = models.IntegerField(blank=True, null=True)
    activities = models.TextField(blank=True)

    objects = LessonManager()

    def __str__(self):
        return self.code + " - " + self.title

    class Meta:
        ordering = ['qualification', 'mode', 'order']

    @property
    def short(self):
        """Short respresentation of lesson"""
        return self.code or self.title

    # Replace with enum when we get python3
    LESSON_STATE_NO = ('NO', 'Unplanned')
    LESSON_STATE_PLANNED = ('PLANNED', 'Planned')
    LESSON_STATE_PARTIAL = ('PARTIAL', 'Partially Completed')
    LESSON_STATE_YES = ('YES', 'Completed')

    def get_pls(self, trainee):
        """Return a QS of PLs for a lesson for a particular trainee"""
        return PerformedLesson.objects.filter(trainee=trainee, lesson=self)

    def get_lesson_state(self, trainee):
        """Return the 'highest attained state' of a lesson for a particular trainee"""
        high_state = Lesson.LESSON_STATE_NO
        for pl in self.get_pls(trainee):
            if pl.completed:
                return Lesson.LESSON_STATE_YES
            if pl.partially_completed:
                high_state = Lesson.LESSON_STATE_PARTIAL
            else:
                high_state = Lesson.LESSON_STATE_PLANNED
        return high_state

    def is_completed(self, mp):
        pl = PerformedLesson.objects.filter(trainee=mp, lesson=self, completed=True).count()
        return (pl > 0)

    def is_planned(self, mp):
        pl = PerformedLesson.objects.filter(trainee=mp, lesson=self, completed=False).count()
        return (pl > 0)

    def is_partially_completed(self, mp):
        pl = PerformedLesson.objects.filter(trainee=mp, lesson=self, partially_completed=True, completed=False).count()
        return (pl > 0)


class PerformedLessonManager(models.Manager):
    def get_lessons(self, trainee, lesson=None, completed=None, partially_completed=None):
        pls = self.filter(trainee=trainee)
        if lesson is not None:
            pls = pls.filter(lesson=lesson)
        if completed is not None:
            pls = pls.filter(completed=completed)
        if partially_completed is not None:
            pls = pls.filter(partially_completed=partially_completed)
        return pls

    def get_teaching(self, instructor, lesson=None, completed=None,
                     partially_completed=None):
        pls = self.filter(instructor=instructor)
        if lesson is not None:
            pls = pls.filter(lesson=lesson)
        if completed is not None:
            pls = pls.filter(completed=completed)
        if partially_completed is not None:
            pls = pls.filter(partially_completed=partially_completed)
        return pls


class PerformedLessonPermissions(ModelPermissions):
    def can_view(self, user):
        """Trainee, all instructors and all training officers can view PLs"""
        return (self.instance.trainee == user.profile) or is_instructor(user) or is_training(user)

    def can_view_private(self, user):
        """All instructors and training officers can view private notes"""
        return is_instructor(user) or is_training(user)

    def get_private_notes(self, user):
        """Proxy method to access private notes"""
        if self.can_view_private(user):
            return self.instance.private_notes
        else:
            return None

    def can_edit(self, user):
        """The named instructor and all training officers can edit PLs"""
        return (self.instance.instructor == user.profile) or is_training(user)

    def can_delete(self, user):
        return self.can_edit(user)


@reversion.register()
class PerformedLesson(ModelComposeMixin, models.Model):
    session = models.ForeignKey('Session', blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True, null=True)
    lesson = models.ForeignKey('Lesson', blank=True, null=True, on_delete=models.PROTECT)
    instructor = models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_instructor", blank=True, null=True,
                                   limit_choices_to={'is_instructor_cached': True}, on_delete=models.SET_NULL)
    trainee = models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_trainee", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    partially_completed = models.BooleanField(default=False)
    public_notes = models.TextField(blank=True)
    private_notes = models.TextField(blank=True)

    objects = PerformedLessonManager()

    compose_classes = {
        'permissions': PerformedLessonPermissions
    }
    permissions = None # type: PerformedLessonPermissions

    def uid(self):
        return "PL{:0>4d}".format(self.pk)

    @property
    def state(self):
        """Return the state of this PL"""
        if self.completed:
            return Lesson.LESSON_STATE_YES
        elif self.partially_completed:
            return Lesson.LESSON_STATE_PARTIAL
        else:
            return Lesson.LESSON_STATE_PLANNED

    # TODO remove
    def get_date(self):
        return self.date  # legacy, will be removed

    def save(self, *args, **kwargs):
        if self.session:
            self.date = self.session.when.date()
        super(PerformedLesson, self).save(*args, **kwargs)

    class Meta:
        ordering = ['trainee__last_name', 'date']
        get_latest_by = "date"


@reversion.register()
class Session(models.Model):
    LESSON_HISTORY = datetime.timedelta(weeks=2)

    name = models.CharField(max_length=64, blank=True, help_text='Optional name for session')
    when = models.DateTimeField(help_text='Formatted like: DD/MM/YYYY HH:MM')
    where = models.ForeignKey('xsd_sites.Site', blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, help_text='Viewable by instructors and trainees in session.')

    completed = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            # return "'" + self.name + "' " + self.when.strftime('%a %d %b %Y %H:%M') + " at " + self.where.__str__()
            return "{} '{}' {} at {}".format(self.uid(), self.name, self.when.strftime('%a %d %b %Y %H:%M'), self.where)
        else:
            return "{} {} at {}".format(self.uid(), self.when.strftime('%a %d %b %Y %H:%M'), self.where)

    def get_absolute_url(self):
        return reverse('xsd_training:SessionPlanner', kwargs={'pk': self.pk})

    def uid(self):
        return "S{:0>4d}".format(self.pk)

    def in_past(self):
        return self.when.replace(tzinfo=None) < datetime.datetime.now()

    def add_trainees(self, trainees):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Added trainees')
            self._add_pls(trainees)

    def add_trainee_group(self, tg):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Added group {}'.format(tg.name))
            self._add_pls(tg.trainees.all())

    def _add_pls(self, trainees):
        """Add blank Performed Lessons to Session"""
        for trainee in trainees:
            PerformedLesson.objects.create(
                session=self,
                trainee=trainee,
            )

    def save(self, *args, **kwargs):
        return super(Session, self).save(*args, **kwargs)

    class Meta:
        ordering = ['when']
