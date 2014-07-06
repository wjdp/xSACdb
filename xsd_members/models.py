from django.db import models
from datetime import date

from django_facebook.models import FacebookModel

from xsd_training.models import PerformedLesson

class MemberProfile(FacebookModel):
    user = models.OneToOneField('auth.User')
    token = models.CharField(max_length=150, blank=True)
    new = models.BooleanField(default=True)
    new_notify = models.BooleanField(default=True)

    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=11, blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    
    next_of_kin_name = models.CharField(max_length=40, blank=True)
    next_of_kin_relation = models.CharField(max_length=20, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)

    veggie = models.BooleanField(default=False, verbose_name='Vegetarian')
    alergies = models.TextField(blank=True, verbose_name='Alergies and other requiements')

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

    bsac_id=models.IntegerField(max_length=7,blank=True, null=True, verbose_name=u'BSAC ID')
    bsac_expiry=models.DateField(blank=True, null=True, verbose_name=u'BSAC Expiry')
    bsac_direct_member=models.BooleanField(default=False, verbose_name=u'BSAC Direct Member', help_text='Adjusts the wording presented to the member when BSAC expires.')
    bsac_member_via_another_club=models.BooleanField(default=False, verbose_name=u'BSAC member via another club', help_text='Adjusts the wording presented to the member when BSAC expires.' )
    bsac_direct_debit=models.BooleanField(default=False, verbose_name=u'BSAC Direct Debit')

    medical_form_expiry=models.DateField(blank=True, null=True)

    other_qualifications = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    _top_qual_cached = None
    def top_qual(self):
        if self._top_qual_cached:
            return self._top_qual_cached
        else:
            if self.qualifications.count()==0: return None
            q=self.qualifications.all().exclude(instructor_qualification=True)
            c=q.count()-1
            if c >= 0:
                self._top_qual_cached = q[c]
                return q[c]
            else:
                return None

    _top_instructor_qual_cached = None
    def top_instructor_qual(self):
        if self._top_instructor_qual_cached:
            return self._top_instructor_qual_cached
        else:
            q=self.qualifications.all().filter(instructor_qualification=True)
            if q.count()==0: return None
            c=q.count()-1
            self._top_instructor_qual_cached = q[c]
            return self.top_instructor_qual()
    
    _is_instructor_cached = None
    def is_instructor(self):
        if _is_instructor_cached:
            return _is_instructor_cached
        else:
            if self.top_instructor_qual()==None:
                _is_instructor_cached = False
            else:
                _is_instructor_cached = True
            self.is_instructor()

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
    def performed_lesson_ramble(self):
        pls =  PerformedLesson.objects.filter(trainee=self.user)
        ret = ""
        for pl in pls:
            ret += pl.lesson.code+' - '+str(pl.date)+'<br />'
        return ret[:len(ret)-6]

    def missing_personal_details(self):
        if self.dob==None or self.address==None or self.postcode==None or self.home_phone==None \
        or self.mobile_phone==None or self.next_of_kin_name==None or self.next_of_kin_relation==None \
        or self.next_of_kin_relation==None or self.next_of_kin_phone==None:
            return True
        else:
            return False

    def dob(self):
        return self.date_of_birth

    def age(self):
        today=date.today()
        num_years = int((today - self.date_of_birth).days / 365.25)
        return num_years
    def formatted_address(self):
        return self.address.replace("\n","<br />")
    def formatted_other_qualifications(self):
        return self.other_qualifications.replace("\n","<br />")
    def formatted_alergies(self):
        return self.alergies.replace("\n","<br />")

    def heshe(self):
        if self.gender=="m": return "He"
        if self.gender=="f": return "She"
        return "They"

    def upcoming_sdcs(self):
        from xsd_training.models import PerformedSDC
        return PerformedSDC.objects.filter(trainees=self.user, completed=False)

    _cached_user_group_values = 0
    def user_groups_values(self):
        if self._cached_user_group_values != 0:
            return self._cached_user_group_values
        else:
            self._cached_user_group_values = [x['id'] for x in self.user.groups.all().values()]
            return self.user_groups_values()


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
