from django.db import models
import django.contrib.auth

class PerformedLesson(models.Model):
    session=models.ForeignKey('Session', blank=True, null=True)
    date=models.DateField(blank=True, null=True)
    lesson=models.ForeignKey('Lesson')
    instructor=models.ForeignKey('auth.User', related_name="pl_instructor")
    trainee=models.ForeignKey('auth.User', related_name="pl_trainee")
    completed=models.BooleanField(default=False)
    public_notes=models.TextField(blank=True)
    private_notes=models.TextField(blank=True)

    #def __unicode__(self):
    #    ret = ("Lesson " + self.lesson.code + " at " +
    #           str(self.session.when) + " instr by " +
    #           self.instructor.first_name + " " + self.instructor.last_name)
    def get_date(self):
        if self.date==None:
            return self.session.when.date()
        else:
            return self.date

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
        ordering = ['qualification','order']

    def is_completed(self, user):
        pl=PerformedLesson.objects.filter(trainee=user, lesson=self, completed=True).count()
        if pl>0: return True
        else: return False

class Qualification(models.Model):
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

class SDC(models.Model):
    title=models.CharField(max_length=50)
    min_qualification=models.ForeignKey('Qualification', blank=True, null=True)

    def __unicode__(self): return self.title

    class Meta:
        verbose_name="SDC"
        verbose_name_plural="SDCs"
        ordering=['title']

class Session(models.Model):
    when=models.DateTimeField()
    where=models.ForeignKey('xsd_sites.Site')
    notes=models.TextField(blank=True)
    created_by=models.ForeignKey('auth.User')

    def __unicode__(self):
        return str(self.when) + " at " + self.where.__unicode__()
