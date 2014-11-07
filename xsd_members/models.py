from django.db import models
from datetime import date

from django_facebook.models import FacebookModel

from xsd_training.models import PerformedLesson
from xSACdb.data_helpers import disable_for_loaddata

class MemberProfile(FacebookModel):
    user = models.OneToOneField('auth.User')
    token = models.CharField(max_length=150, blank=True)
    new = models.BooleanField(default=True)

    # This is being used to 'approve' new members
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

    top_qual_cached = models.ForeignKey('xsd_training.Qualification', blank=True, null=True, related_name='top_qual_cached')
    def top_qual(self, nocache = False):
        if nocache:
            if self.qualifications.count()==0: return None
            q=self.qualifications.all().exclude(instructor_qualification=True)
            c=q.count()-1
            if c >= 0:
                return q[c]
            else:
                return None
        else:
            return self.top_qual_cached

    top_instructor_qual_cached = models.ForeignKey('xsd_training.Qualification', blank=True, null=True, related_name='top_instructor_qual_cached')
    def top_instructor_qual(self, nocache = False):
        if nocache:
            q=self.qualifications.all().filter(instructor_qualification=True)
            if q.count()==0: return None
            c=q.count()-1
            return q[c]
        else:
            return self.top_instructor_qual_cached

    is_instructor_cached = models.NullBooleanField(default=None, blank=True)
    def is_instructor(self, nocache = False):
        if nocache:
            if self.top_instructor_qual()==None:
                # No instructor quals, not an instructor
                return False
            else:
                # instructor quals, is an instructor
                return True
        else:
            return self.is_instructor_cached

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
        # TODO: A good comment here would be ideal!
        pls =  PerformedLesson.objects.filter(trainee=self.user)
        ret = ""
        for pl in pls:
            ret += pl.lesson.code+' - '+str(pl.date)+'<br />'
        return ret[:len(ret)-6]

    PERSONAL_FIELDS = ['address','postcode','home_phone','mobile_phone','next_of_kin_name','next_of_kin_relation','next_of_kin_phone']

    def missing_personal_details(self):
        """If missing any personal details, flag up"""
        for field in self.PERSONAL_FIELDS:
            field_value = getattr(self, field)
            if field_value == None or field_value == "":
                return True
        return False

    def dob(self):
        """Alias for date_of_birth"""
        return self.date_of_birth

    def age(self):
        """Calculate age, we ignore leap days/seconds etc and just
        work out the 'social' age of the person"""
        if self.date_of_birth:
            today=date.today()
            year_diff = today.year - self.date_of_birth.year
            if today.month <= self.date_of_birth.month and \
                today.day < self.date_of_birth.day:
                # It's before this years birthday
                age = year_diff - 1
            else:
                age = year_diff

            return age
        else:
            # No DOB recorded.
            return None
    def formatted_address(self):
        """Return address with html <br /> instead of line breaks"""
        return self.address.replace("\n","<br />")
    def formatted_other_qualifications(self):
        """Return other qualifications with html <br /> instead of line breaks"""
        return self.other_qualifications.replace("\n","<br />")
    def formatted_alergies(self):
        """Return allergies with html <br /> instead of line breaks"""
        return self.alergies.replace("\n","<br />")

    def heshe(self):
        """Returns a Proper capitalised pronoun for the user"""
        if self.gender=="m": return "He"
        if self.gender=="f": return "She"
        return "They"

    def set_qualification(self, qual):
        """Adds the qualification qual, if qual is lower than top_qual then
        the higher qualifications are removed"""
        instructor = qual.instructor_qualification

        to_remove = self.qualifications.filter(
            instructor_qualification = instructor,
            rank__gt = qual.rank,
        )

        for q in to_remove:
            self.qualifications.remove(q)

        self.qualifications.add(qual)

    def remove_qualifications(self, instructor=False):
        quals = self.qualifications.filter(
            instructor_qualification = instructor
        )
        for q in quals:
            self.qualifications.remove(q)

        if instructor:
            self.instructor_number=None

    def add_sdc(self, sdc):
        if not sdc in self.sdcs.all():
            self.sdcs.add(sdc)

    def upcoming_sdcs(self):
        """Return upcoming SDCs for the user, does this belong here?"""
        from xsd_training.models import PerformedSDC
        return PerformedSDC.objects.filter(trainees=self.user, completed=False)

    _cached_user_group_values = 0
    def user_groups_values(self):
        if self._cached_user_group_values != 0:
            return self._cached_user_group_values
        else:
            self._cached_user_group_values = [x['id'] for x in self.user.groups.all().values()]
            return self.user_groups_values()

    def save(self, *args, **kwargs):
        if self.pk:
            self.cache_update()
        super(MemberProfile, self).save(*args, **kwargs)
    def cache_update(self):
        """Compute and write the cached fields"""
        self.top_qual_cached = self.top_qual(nocache=True)
        self.top_instructor_qual_cached = self.top_instructor_qual(nocache=True)
        self.is_instructor_cached = self.is_instructor(nocache=True)

from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Make sure we create a MemberProfile when creating a User
@disable_for_loaddata
def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)

class MembershipType(models.Model):
    name=models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

# class Mailing(models.Model):
#     title = models.CharField(max_length=64)
#     sender = models.ForeignKey('auth.User', related_name='sender')
#     recipients = models.ManyToManyField('auth.User', related_name='recipients_set')
#     message = models.TextField()
#     is_public = models.BooleanField(help_text='Message can be viewed by all members')

#     class Meta:
#         verbose_name = 'Mailing'
#         verbose_name_plural = 'Mailings'

#     def __unicode__(self):
#         pass

