from django.db import models
import django.contrib.auth

class PerformedLesson(models.Model):
    session=models.ForeignKey('Session')
    lesson=models.ForeignKey('Lesson')
    instructor=models.ForeignKey('auth.User', related_name="pl_instructor")
    trainees=models.ManyToManyField('auth.User', related_name="pl_trainees")
    completed=models.BooleanField(default=False)
    private_notes=models.TextField(blank=True)

    def __unicode__(self):
        ret = ("Lesson " + self.lesson.code + " at " +
               self.session.when + " instr by " +
               self.instructor.first_name + " " + self.instructor.last_name)

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
                   )
    qualification = models.ForeignKey('Qualification')
    code = models.CharField(max_length=5)
    title = models.CharField(max_length=30)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    description=models.TextField(blank=True)
    max_depth=models.IntegerField(blank=True, null=True)
    activities=models.TextField(blank=True)
    
    def __unicode__(self):
        return self.code + " - " + self.title

class Qualification(models.Model):
    title=models.CharField(max_length=30)
    rank=models.IntegerField()
    definition=models.TextField(blank=True)
    instructor_qualification=models.BooleanField(default=False)

    def __unicode__(self): return self.title

class SDC(models.Model):
    title=models.CharField(max_length=50)
    min_qualification=models.ForeignKey('Qualification')

    def __unicode__(self): return title

class Session(models.Model):
    when=models.DateTimeField()
    where=models.ForeignKey('xsd_sites.Site')
    notes=models.TextField(blank=True)
    created_by=models.ForeignKey('auth.User')
