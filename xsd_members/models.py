from django.db import models
from datetime import date

from django_facebook.models import FacebookProfileModel

from xsd_training.models import PerformedLesson

class MemberProfile(models.Model):
    user = models.OneToOneField('auth.User')
    gender = models.CharField(max_length=6, blank=True)
    facebook_id = models.BigIntegerField(verbose_name=u'Facebook ID',blank=True,null=True)
    token = models.CharField(max_length=150, blank=True)

    dob = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=11, blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    
    next_of_kin_name = models.CharField(max_length=40, blank=True)
    next_of_kin_relation = models.CharField(max_length=20, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)

    veggie = models.BooleanField(default=False)
    alergies = models.TextField(blank=True)

    qualifications=models.ManyToManyField('xsd_training.Qualification', blank=True)
    training_for=models.ForeignKey('xsd_training.Qualification', blank=True, null=True, related_name='q_training_for')
    sdcs=models.ManyToManyField('xsd_training.SDC', blank=True)
    instructor_number=models.IntegerField(blank=True, null=True)
    
    student_id=models.IntegerField(max_length=7,blank=True, null=True)
    
    associate_id=models.IntegerField(max_length=7,blank=True, null=True)
    associate_expiry=models.DateField(blank=True, null=True)

    club_id=models.IntegerField(max_length=7,blank=True, null=True)
    club_expiry=models.DateField(blank=True, null=True)
    club_membership_type=models.ForeignKey('MembershipType', blank=True, null=True)

    bsac_id=models.IntegerField(max_length=7,blank=True, null=True)
    bsac_expiry=models.DateField(blank=True, null=True)
    bsac_direct_member=models.BooleanField(default=False)
    bsac_member_via_another_club=models.BooleanField(default=False)
    bsac_direct_debit=models.BooleanField(default=False)

    medical_form_expiry=models.DateField(blank=True, null=True)

    other_qualifications = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    def top_qual(self):
        if self.qualifications.count()==0:
            print "i returned none"
            return None
        q=self.qualifications.all().exclude(instructor_qualification=True)
        c=q.count()-1
        return q[c]

    def club_expired(self):
        if self.club_expiry==None or self.club_expiry <= date.today(): return True
        else: return False
    def bsac_expired(self):
        if self.bsac_expiry==None or self.bsac_expiry <= date.today(): return True
        else: return False
    def medical_form_expired(self):
        if self.medical_form_expiry==None or self.medical_form_expiry <= date.today(): return True
        else: return False
    def membership_problem(self):
        if self.club_expired() or self.bsac_expired() or self.medical_form_expired():
            return True
        else: return False
    def no_expiry_data(self):
        if self.club_expiry==None and self.bsac_expiry==None and self.medical_form_expiry==None:
            return True
        else: return False
    def performed_lessons_for_qualification(self, qualification):
        pass

    def missing_personal_details(self):
        if self.dob==None or self.address==None or self.postcode==None or self.home_phone==None \
        or self.mobile_phone==None or self.next_of_kin_name==None or self.next_of_kin_relation==None \
        or self.next_of_kin_relation==None or self.next_of_kin_phone==None:
            return True
        else:
            return False

    def age(self):
        today=date.today()
        num_years = int((today - self.dob).days / 365.25)
        return num_years
    def formatted_address(self):
        return self.address.replace("\n","<br />")
    def formatted_other_qualifications(self):
        return self.other_qualifications.replace("\n","<br />")
    def formatted_alergies(self):
        return self.alergies.replace("\n","<br />")

from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser")

from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Make sure we create a MemberProfile when creating a User
def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)

class MembershipType(models.Model):
    name=models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
