from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction
from reversion import revisions as reversion


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


@reversion.register()
class PerformedLesson(models.Model):
    session = models.ForeignKey('Session', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    lesson = models.ForeignKey('Lesson', blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_instructor", blank=True, null=True,
                                   limit_choices_to={'is_instructor_cached': True})
    trainee = models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_trainee")
    completed = models.BooleanField(default=False)
    partially_completed = models.BooleanField(default=False)
    public_notes = models.TextField(blank=True)
    private_notes = models.TextField(blank=True)

    objects = PerformedLessonManager()

    def uid(self):
        return "PL{:0>4d}".format(self.pk)

    # TODO remove
    def get_date(self):
        return self.date  # legacy, will be removed

    def save(self, *args, **kwargs):
        if self.session:
            self.date = self.session.when.date()
        super(PerformedLesson, self).save(*args, **kwargs)

    class Meta:
        ordering = ['trainee__last_name']
        get_latest_by = "date"


class LessonManager(models.Manager):
    def by_qualification_detailed(self, qualification):
        """Return a list of tuples (mode, lessons)"""

        def map_mode_to_lessons(mode):
            lessons_in_mode = self.filter(qualification=qualification, mode=mode[0])
            return (mode, lessons_in_mode)

        key = "by_qualification_detailed--{qualification}".format(qualification=qualification.code)
        val = cache.get(key)
        if val is None:
            val = map(map_mode_to_lessons, Lesson.MODE_CHOICES)
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
    qualification = models.ForeignKey('Qualification')
    code = models.CharField(max_length=5, blank=True)
    title = models.CharField(max_length=90)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    max_depth = models.IntegerField(blank=True, null=True)
    activities = models.TextField(blank=True)

    objects = LessonManager()

    def __unicode__(self):
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
        """Return the 'highest attained state' of a lesson for a particualar trainee"""
        high_state = self.LESSON_STATE_NO
        for pl in self.get_pls(trainee):
            if pl.completed:
                return self.LESSON_STATE_YES
            if pl.partially_completed:
                high_state = self.LESSON_STATE_PARTIAL
            else:
                high_state = self.LESSON_STATE_PLANNED
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


class Qualification(models.Model):
    code = models.CharField(max_length=4, unique=True)
    title = models.CharField(max_length=50)
    rank = models.IntegerField()
    definition = models.TextField(blank=True)
    instructor_qualification = models.BooleanField(default=False)

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
    mode = models.CharField(max_length=3, choices=MODE_CHOICES)
    xo_from = models.CharField(max_length=64, blank=True, null=True)

    signed_off_on = models.DateField(blank=True, null=True)
    signed_off_by = models.ForeignKey('xsd_members.MemberProfile', on_delete=models.PROTECT, blank=True, null=True,
                                      related_name='pqs_signed')

    # TODO: Add instructor_number here, migrate data from MemberProfiles

    notes = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    def uid(self):
        return "PQ{:0>4d}".format(self.pk)

    @property
    def mode_display(self):
        for mode in self.MODE_CHOICES:
            if mode[0] == self.mode:
                return mode[1]
        raise ValueError('Mode not in MODE_CHOICES')


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

    def __unicode__(self):
        return self.title

    def uid(self):
        return "PS{:0>4d}".format(self.pk)

    class Meta:
        verbose_name = "SDC"
        verbose_name_plural = "SDCs"
        ordering = ['title']


class SDCCategoryList(object):
    cat_id = ""
    cat_name = ""
    sdcs = []

    def __init__(self, cat_id, cat_name):
        self.cat_id = cat_id
        self.cat_name = cat_name


class SDCDisplay(object):
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

    def __unicode__(self):
        if self.datetime:
            return "{} @ {}".format(self.sdc, self.datetime)
        else:
            return "{} @ TBD".format(self.sdc)

    def uid(self):
        return "PSDC{:0>4d}".format(self.pk)

    def get_absolute_url(self):
        return reverse('xsd_training:PerformedSDCDetail', kwargs={'pk': self.pk})


@reversion.register()
class Session(models.Model):
    name = models.CharField(max_length=64, blank=True, help_text='Optional name for session')
    when = models.DateTimeField(help_text='Formatted like: DD/MM/YYYY HH:MM')
    where = models.ForeignKey('xsd_sites.Site')
    notes = models.TextField(blank=True, help_text='Viewable by instructors and trainees in session.')

    completed = models.BooleanField(default=False)

    def __unicode__(self):
        if self.name:
            # return "'" + self.name + "' " + self.when.strftime('%a %d %b %Y %H:%M') + " at " + self.where.__unicode__()
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


@reversion.register()
class TraineeGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    trainees = models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)

    TRAINEE_ORDER_BY = 'last_name'

    def __unicode__(self):
        return "{} {}".format(self.uid(), self.name)

    def uid(self):
        return "TG{:0>4d}".format(self.pk)

    def trainees_list(self):
        """returns a readable list of trainee full names separated by commas"""
        ret = ""
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret = ret + t.get_full_name() + ", "

        # chop off trailing comma
        return ret[:-2]

    def trainees_list_with_links(self):
        ret = ''
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret += '<a href=\"' + reverse('xsd_training:TraineeNotes', kwargs={'pk': t.pk}) + '\">' + \
                   t.get_full_name() + '</a>, '
        return ret[:-2]

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

    def get_all_trainees(self):
        return self.trainees.all().order_by(self.TRAINEE_ORDER_BY)

    def get_absolute_url(self):
        return reverse('xsd_training:TraineeGroupUpdate', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
