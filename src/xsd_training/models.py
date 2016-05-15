from __future__ import unicode_literals

import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

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


class PerformedLesson(models.Model):
    session=models.ForeignKey('Session', blank=True, null=True)
    date=models.DateField(blank=True, null=True)
    lesson=models.ForeignKey('Lesson', blank=True, null=True)
    instructor=models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_instructor", blank=True, null=True, limit_choices_to={'is_instructor_cached':True})
    trainee=models.ForeignKey(settings.AUTH_PROFILE_MODEL, related_name="pl_trainee")
    completed=models.BooleanField(default=False)
    partially_completed=models.BooleanField(default=False)
    public_notes=models.TextField(blank=True)
    private_notes=models.TextField(blank=True)

    objects = PerformedLessonManager()

    #def __unicode__(self):
    #    ret = ("Lesson " + self.lesson.code + " at " +
    #           str(self.session.when) + " instr by " +
    #           self.instructor.first_name + " " + self.instructor.last_name)

    def uid(self):
        return "PL{:0>4d}".format(self.pk)

    def get_date(self):
        return self.date  # legacy, will be removed

    def save(self, *args, **kwargs):
        if self.session:
            self.date=self.session.when.date()
        super(PerformedLesson, self).save(*args, **kwargs)

    class Meta:
        ordering=['trainee__last_name']

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
    description=models.TextField(blank=True)
    max_depth=models.IntegerField(blank=True, null=True)
    activities=models.TextField(blank=True)

    def __unicode__(self):
        return self.code + " - " + self.title

    class Meta:
        ordering = ['qualification','mode','order']

    def is_completed(self, mp):
        pl=PerformedLesson.objects.filter(trainee=mp, lesson=self, completed=True).count()
        if pl>0: return True
        else: return False

    def is_planned(self, mp):
        pl=PerformedLesson.objects.filter(trainee=mp, lesson=self, completed=False).count()
        if pl>0: return True
        else: return False

    def is_partially_completed(self, mp):
        pl=PerformedLesson.objects.filter(trainee=mp, lesson=self, partially_completed=True, completed=False).count()
        if pl>0: return True
        else: return False

class Qualification(models.Model):
    code=models.CharField(max_length=4, unique=True)
    title=models.CharField(max_length=50)
    rank=models.IntegerField()
    definition=models.TextField(blank=True)
    instructor_qualification=models.BooleanField(default=False)

    def __unicode__(self): return self.title

    class Meta:
        ordering = ['rank']

    def lessons_by_mode(self, mode):
        lessons=Lesson.objects.filter(qualification=self, mode=mode)
        return lessons

SDC_TYPE_CHOICES = (
    ('clu','Club Diving'),
    ('saf','Safety and Rescue'),
    ('sea','Seamanship'),
    ('spe','Special Interest'),
    ('tec','Technical'),
)

class SDC(models.Model):
    title=models.CharField(max_length=50)
    min_qualification=models.ForeignKey('Qualification', blank=True, null=True)
    description=models.TextField(blank=True)
    category=models.CharField(choices=SDC_TYPE_CHOICES, max_length=3)
    other_requirements=models.BooleanField(default=False)

    interested_members=models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)

    def __unicode__(self):
        return self.title

    def uid(self):
        return "PS{:0>4d}".format(self.pk)

    class Meta:
        verbose_name="SDC"
        verbose_name_plural="SDCs"
        ordering=['title']

class SDCCategoryList(object):
    cat_id=""
    cat_name=""
    sdcs=[]

    def __init__(self,cat_id,cat_name):
        self.cat_id=cat_id
        self.cat_name=cat_name

class SDCDisplay(object):
    sdc=None
    can_do=False


class PerformedSDC(models.Model):
    sdc=models.ForeignKey('SDC')
    datetime=models.DateTimeField(blank=True, null=True)
    notes=models.TextField(blank=True)
    trainees=models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)
    completed=models.BooleanField(default=False)
    # places = models.IntegerField()

    def get_absolute_url(self):
        return reverse('PerformedSDCDetail', kwargs={'pk': self.pk})

class Session(models.Model):
    name=models.CharField(max_length=64, blank=True, help_text='Optional name for session')
    when=models.DateTimeField(help_text='Formatted like: DD/MM/YYYY HH:MM')
    where=models.ForeignKey('xsd_sites.Site')
    notes=models.TextField(blank=True, help_text='Viewable by instructors and trainees in session.')

    completed = models.BooleanField(default=False)

    def __unicode__(self):
        if self.name:
            #return "'" + self.name + "' " + self.when.strftime('%a %d %b %Y %H:%M') + " at " + self.where.__unicode__()
            return "{} '{}' {} at {}".format(self.uid(), self.name, self.when.strftime('%a %d %b %Y %H:%M'), self.where)
        else:
            return "{} {} at {}".format(self.uid(), self.when.strftime('%a %d %b %Y %H:%M'), self.where)

    def get_absolute_url(self):
        return reverse('SessionPlanner', kwargs={'pk': self.pk})

    def uid(self):
        return "S{:0>4d}".format(self.pk)

    def in_past(self):
        if self.when.replace(tzinfo=None) < datetime.datetime.now():
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        return super(Session, self).save(*args, **kwargs)

    class Meta:
        ordering=['when']

class TraineeGroup(models.Model):
    name=models.CharField(max_length=64, unique=True)
    trainees=models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)

    TRAINEE_ORDER_BY='last_name'

    def __unicode__(self):
        return "{} {}".format(self.uid(), self.name)

    def uid(self):
        return "TG{:0>4d}".format(self.pk)

    def trainees_list(self):
        """returns a readable list of trainee full names separated by commas"""
        ret=""
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret=ret+t.get_full_name()+", "

        # chop off trailing comma
        return ret[:-2]

    def trainees_list_with_links(self):
        ret=''
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret += '<a href=\"' + reverse('TraineeNotes', kwargs={'pk':t.pk}) + '\">' + \
                t.get_full_name() + '</a>, '
        return ret[:-2]

    def get_all_trainees(self):
        return self.trainees.all().order_by(self.TRAINEE_ORDER_BY)

    class Meta:
        ordering=['name']
