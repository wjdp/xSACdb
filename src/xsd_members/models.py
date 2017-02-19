from __future__ import unicode_literals

import random
import warnings
from datetime import date

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction
from reversion import revisions as reversion
from actstream import action

from xSACdb.data_helpers import disable_for_loaddata
from xsd_training.models import PerformedLesson


class DateOfBirthField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(**kwargs)
        return super(DateOfBirthField, self).formfield(**defaults)


class MemberProfileManager(models.Manager):
    def all(self):
        # Filtering is applied here to hide 'hidden' users
        return super(MemberProfileManager, self).all().exclude(hidden=True)

    def all_actual(self):
        return super(MemberProfileManager, self).all()


@reversion.register()
class MemberProfile(models.Model):
    """Model for representing members of the club, a user account has a O2O
    relationship with this profile. The profile 'should' be able to exist
    without a user."""

    objects = MemberProfileManager()

    # Fields to ensure we have, will present member with form to fill in on login. Can be added to without breaking
    # things on upgrade.
    REQUIRED_FIELDS = (
        'date_of_birth',
        'gender',
        'address',
        'postcode',
        'home_phone',
        'mobile_phone',
        'next_of_kin_name',
        'next_of_kin_relation',
        'next_of_kin_phone',
    )
    # Fields shown with above, but as can be blank we can't require them
    OPTIONAL_FIELDS = (
        'veggie',
        'alergies',
    )

    # What is personal data? This is used for expunging member's records.
    PERSONAL_DATA = REQUIRED_FIELDS + OPTIONAL_FIELDS

    class Meta:
        ordering = ['last_name', 'first_name']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True,
                                blank=True)

    # Used to hide users from 'all' queries.
    hidden = models.BooleanField(default=False)

    # FIXME Not really sure if this is needed?
    token = models.CharField(max_length=150, blank=True)

    # This is being used to 'approve' new members
    new_notify = models.BooleanField(default=True)

    @property
    def verified(self):
        return not self.new_notify

    def approve(self, actor=None):
        """
        Set whatever property we need to approve this member.
        """
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Approved member')
            if actor:
                action.send(actor, verb='approved', action_object=self)
            self.new_notify = False
            self.save()

    # Migrated from user model
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    # Profile details
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)

    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=11, blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)

    next_of_kin_name = models.CharField(max_length=40, blank=True,
                                        help_text="For an sport such as diving the practical activities involve some \
                                        level of risk, as such <strong>next of kin</strong> details are kept in case of\
                                         emergency. This data is only accessed when required. It will be taken in paper\
                                         form on trips.")
    next_of_kin_relation = models.CharField(max_length=20, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)

    veggie = models.NullBooleanField(default=None, verbose_name='Vegetarian', help_text="Gives an indication to trip \
                                                                                organisers for food requirements.")

    # FIXME spelling
    alergies = models.TextField(blank=True, verbose_name='Allergies and other requirements',
                                help_text="This information is held for use by trip organisers. Please note anything \
                                           that would be important for both underwater activities and general trips, \
                                           details are held in confidence.")

    qualifications = models.ManyToManyField('xsd_training.Qualification', blank=True)
    training_for = models.ForeignKey('xsd_training.Qualification', blank=True, null=True, related_name='q_training_for')
    sdcs = models.ManyToManyField('xsd_training.SDC', blank=True)
    instructor_number = models.IntegerField(blank=True, null=True)

    student_id = models.IntegerField(blank=True, null=True)

    associate_id = models.IntegerField(blank=True, null=True)
    associate_expiry = models.DateField(blank=True, null=True)

    club_id = models.IntegerField(blank=True, null=True)
    club_expiry = models.DateField(blank=True, null=True)
    club_membership_type = models.ForeignKey('MembershipType', blank=True, null=True)

    bsac_id = models.IntegerField(blank=True, null=True, verbose_name=u'BSAC ID')
    bsac_expiry = models.DateField(blank=True, null=True, verbose_name=u'BSAC Expiry')
    bsac_direct_member = models.BooleanField(default=False, verbose_name=u'BSAC Direct Member',
                                             help_text='Adjusts the wording presented to the member when BSAC expires.')
    bsac_member_via_another_club = models.BooleanField(default=False, verbose_name=u'BSAC member via another club',
                                                       help_text='Adjusts the wording presented to the member when \
                                                       BSAC membership expires.')
    bsac_direct_debit = models.BooleanField(default=False, verbose_name=u'BSAC Direct Debit')

    medical_form_expiry = models.DateField(blank=True, null=True)

    other_qualifications = models.TextField(blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('xsd_members:MemberDetail', kwargs={'pk': self.pk})

    def uid(self):
        return "M{:0>4d}".format(self.pk)

    top_qual_cached = models.ForeignKey('xsd_training.Qualification', blank=True, null=True,
                                        related_name='top_qual_cached')

    def top_qual(self, nocache=False):
        if nocache:
            if self.qualifications.count() == 0: return None
            q = self.qualifications.all().exclude(instructor_qualification=True)
            c = q.count() - 1
            if c >= 0:
                return q[c]
            else:
                return None
        else:
            return self.top_qual_cached

    top_instructor_qual_cached = models.ForeignKey('xsd_training.Qualification', blank=True, null=True,
                                                   related_name='top_instructor_qual_cached')

    def top_instructor_qual(self, nocache=False):
        if nocache:
            q = self.qualifications.all().filter(instructor_qualification=True)
            if q.count() == 0: return None
            c = q.count() - 1
            return q[c]
        else:
            return self.top_instructor_qual_cached

    is_instructor_cached = models.NullBooleanField(default=None, blank=True)

    def is_instructor(self, nocache=False):
        if nocache:
            if self.top_instructor_qual() == None:
                # No instructor quals, not an instructor
                return False
            else:
                # instructor quals, is an instructor
                return True
        else:
            return self.is_instructor_cached

    def club_expired(self):
        if self.club_expiry == None or self.club_expiry <= date.today():
            return True
        else:
            return False

    def bsac_expired(self):
        if self.bsac_expiry == None or self.bsac_expiry <= date.today():
            return True
        else:
            return False

    def medical_form_expired(self):
        if self.medical_form_expiry == None or self.medical_form_expiry <= date.today():
            return True
        else:
            return False

    def membership_problem(self):
        if self.club_expired() or self.bsac_expired() or self.medical_form_expired():
            return True
        else:
            return False

    def no_expiry_data(self):
        if self.club_expiry == None and self.bsac_expiry == None and self.medical_form_expiry == None:
            return True
        else:
            return False

    def performed_lesson_ramble(self):
        # TODO: A good comment here would be ideal!
        pls = PerformedLesson.objects.get_lessons(trainee=self)
        ret = ''
        for pl in pls:
            if pl.lesson:
                ret += pl.lesson.code + ' - ' + str(pl.date) + '<br />'
        return ret[:len(ret) - 6]

    PERSONAL_FIELDS = ['address', 'postcode', 'home_phone', 'mobile_phone', 'next_of_kin_name', 'next_of_kin_relation',
                       'next_of_kin_phone']

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
            today = date.today()
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
        return self.address.replace("\n", "<br />")

    def formatted_other_qualifications(self):
        """Return other qualifications with html <br /> instead of line breaks"""
        return self.other_qualifications.replace("\n", "<br />")

    def formatted_alergies(self):
        """Return allergies with html <br /> instead of line breaks"""
        return self.alergies.replace("\n", "<br />")

    def heshe(self):
        """Returns a Proper capitalised pronoun for the user"""
        if self.gender == "m": return "He"
        if self.gender == "f": return "She"
        return "They"

    def set_qualification(self, qual):
        """Adds the qualification qual, if qual is lower than top_qual then
        the higher qualifications are removed"""
        instructor = qual.instructor_qualification

        to_remove = self.qualifications.filter(
            instructor_qualification=instructor,
            rank__gt=qual.rank,
        )

        for q in to_remove:
            self.qualifications.remove(q)

        # TODO if qual is instructor_qual AND previous, lower ranking instructor
        # qual is present THEN reset the instructor_number

        self.qualifications.add(qual)

    def remove_qualifications(self, instructor=False):
        """Wipes all qualifications"""
        quals = self.qualifications.filter(
            instructor_qualification=instructor
        )
        for q in quals:
            self.qualifications.remove(q)

        if instructor:
            self.instructor_number = None

    def add_sdc(self, sdc):
        if not sdc in self.sdcs.all():
            self.sdcs.add(sdc)

    def upcoming_sdcs(self):
        """Return upcoming SDCs for the user, does this belong here?"""
        from xsd_training.models import PerformedSDC
        return PerformedSDC.objects.filter(trainees=self, completed=False)

    _cached_user_group_values = 0

    def user_groups_values(self):
        if self._cached_user_group_values != 0:
            return self._cached_user_group_values
        else:
            self._cached_user_group_values = [x['id'] for x in self.user.groups.all().values()]
            return self.user_groups_values()

    def memberprofile(self):
        """Legacy bit"""
        warnings.warn("Stop using memberprofile.memberprofile", DeprecationWarning, stacklevel=2)
        return self

    def get_full_name(self):
        """Transfer bit"""
        return u"{} {}".format(self.first_name, self.last_name)

    def date_joined(self):
        """Transfer bit"""
        return self.user.date_joined

    def compute_training_for(self):
        """Work out the highest level of lesson the trainee has done"""
        # Get all PLs for this member, exclude any with no lesson re #102
        pls = PerformedLesson.objects.get_lessons(trainee=self).exclude(lesson__isnull=True)
        top_qual = None

        for pl in pls:
            if pl.lesson.qualification.instructor_qualification:
                # Exclude PLs with instructor lessons
                continue

            if top_qual:
                # Compare levels, set if above
                if pl.lesson.qualification.rank > top_qual.rank:
                    top_qual = pl.lesson.qualification
            else:
                # No top_qual, if there is any data take
                top_qual = pl.lesson.qualification

        # Return the top_qual found via iteration over PLs
        return top_qual

    def update_training_for(self):
        """Update the cached value"""
        computed_qual = self.compute_training_for()
        if computed_qual:
            if self.training_for:
                if computed_qual.rank > self.training_for.rank:
                    self.training_for = computed_qual
            else:
                self.training_for = computed_qual

    def get_missing_field_list(self):
        # Returns a list of stringy fields that need stuff in them, if I return [] then we're all good
        fields_that_need_stuff_in_them = []
        for field_name in self.REQUIRED_FIELDS:
            # Pretty basic validation, is it empty. We may need better in the future, it will plug in here
            if not getattr(self, field_name):
                fields_that_need_stuff_in_them.append(field_name)
        return fields_that_need_stuff_in_them


    def save(self, *args, **kwargs):
        """Saves changes to the model instance"""
        if self.pk:
            self.cache_update()
        if self.pk and self.user:
            self.sync()

        super(MemberProfile, self).save(*args, **kwargs)

    def cache_update(self):
        """Compute and write the cached fields"""
        # TODO replace with django's built in cache system
        self.top_qual_cached = self.top_qual(nocache=True)
        self.top_instructor_qual_cached = self.top_instructor_qual(nocache=True)
        self.is_instructor_cached = self.is_instructor(nocache=True)

    def seed(self, user):
        """Seed a newly created MP with data from the user model"""
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        self.email = self.user.email

    def fake(self, fake):
        self.date_of_birth = fake.date_time_between(start_date="-90y", end_date="-12y", tzinfo=None).date()
        self.gender = random.choice(('m', 'f'))
        self.address = fake.address()
        self.postcode = fake.postcode()
        self.home_phone = fake.phone_number()
        self.mobile_phone = fake.phone_number()
        self.next_of_kin_name = fake.name()
        self.next_of_kin_relation = random.choice(('Mother', 'Father', 'Mum', 'Dad', 'Partner', 'Wife',
                                                                 'Husband', 'Dog', 'Cat', 'Fish', 'Tortoise'))
        self.next_of_kin_phone = fake.phone_number()

        if fake.boolean(chance_of_getting_true=50):
            self.student_id = random.randrange(1234567,9999999)

        self.veggie = fake.boolean(chance_of_getting_true=10)
        if fake.boolean(chance_of_getting_true=50):
            self.alergies = fake.paragraph()

        # Most people are current, 15% are out of date
        if fake.boolean(chance_of_getting_true=85):
            self.club_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
            self.bsac_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
            self.medical_form_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
        else:
            if fake.boolean(chance_of_getting_true=60):
                self.club_expiry = fake.date_time_between(start_date="-6y", end_date="+1y", tzinfo=None).date()
            if fake.boolean(chance_of_getting_true=60):
                self.bsac_expiry = fake.date_time_between(start_date="-6y", end_date="+1y", tzinfo=None).date()
            if fake.boolean(chance_of_getting_true=60):
                self.medical_form_expiry = fake.date_time_between(start_date="-6y", end_date="+3y", tzinfo=None).date()

    def sync(self):
        """Sync the user object with the MP"""
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
        # TODO check if actually changed
        self.user.save()

    # Marks the user as archived.
    archived = models.BooleanField(default=False)

    def archive(self, actor=None):
        """Archive the user, hiding them from most views and removing a lot of personal data."""
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Archived member')
            if actor:
                action.send(actor, verb='archived', action_object=self)
            self.expunge()
            self.archived = True
            self.save()

    def expunge(self):
        """Remove personal data"""
        for field_name in self.PERSONAL_DATA:
            # Clear personal data
            if not self._meta.get_field(field_name).null:
                # Char and Text fields like blank null values
                setattr(self, field_name, '')
            else:
                # Everything else has None
                setattr(self, field_name, None)

    def reinstate(self, actor=None):
        """Opposite of archive"""
        # self.hidden = False # Seems this is too aggressive
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Restored member')
            if actor:
                action.send(actor, verb='restored', action_object=self)
            self.archived = False
            self.save()


    def delete(self):
        # When MP is deleted, we should also remove the user attached to it.
        # Soon we will 'archive' profiles, rather than deleting them.
        user = self.user
        super(MemberProfile, self).delete()
        user.delete()


from django.db.models.signals import post_save


# Make sure we create a MemberProfile when creating a User
@disable_for_loaddata
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        mp = MemberProfile.objects.create(user=instance)
        mp.seed(instance)
        mp.save()
        instance.follow_defaults()


post_save.connect(create_member_profile, sender=settings.AUTH_USER_MODEL)


# Update training_for when a PerformedLesson is updated
@disable_for_loaddata
def trigger_update_training_for(sender, instance, created, **kwargs):
    if instance.trainee and instance.lesson:
        mp = instance.trainee
        mp.update_training_for()
        mp.save()


post_save.connect(trigger_update_training_for, sender=PerformedLesson)


class MembershipType(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
