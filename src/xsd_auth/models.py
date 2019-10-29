

import hashlib
import random
import warnings

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import UserManager as DJ_UserManager
from django.db import transaction
from django.utils.functional import cached_property

from xSACdb.cache import object_cached_property, ObjectPropertyCacheInvalidationMixin
from xSACdb.roles.groups import GROUP_ADMIN


class UserManager(DJ_UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            username = random.randrange(1000000000000000, 9999999999999999)

        return super(UserManager, self).create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        with transaction.atomic():
            su = DJ_UserManager.create_superuser(self, username, email, password, **extra_fields)
            su.profile.new_notify = False
            su.profile.save()
            su.groups.add(Group.objects.get(pk=GROUP_ADMIN))
            su.save()
        return su

    def fake_single(self, fake, approved=True):
        """Create a fake user and return"""
        user = self.create_user(
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        user.save()
        user.memberprofile.new_notify = not approved
        user.memberprofile.date_of_birth = fake.date_time_between(start_date='-99y', end_date='now').date()
        user.memberprofile.gender = random.choice(('m', 'f'))
        user.memberprofile.address = fake.address()
        user.memberprofile.postcode = fake.postcode()
        user.memberprofile.home_phone = fake.phone_number()
        user.memberprofile.mobile_phone = fake.phone_number()
        user.memberprofile.next_of_kin_name = fake.name()
        user.memberprofile.next_of_kin_relation = fake.first_name()
        user.memberprofile.next_of_kin_phone = fake.phone_number()
        user.memberprofile.save()
        return user


from actstream.actions import follow


class UserActivityMixin(object):
    def follow_defaults(self):
        follow(self, self.profile, send_action=False, actor_only=False)


class User(UserActivityMixin,
           ObjectPropertyCacheInvalidationMixin,
           AbstractUser):
    """User subclass for xSACdb"""

    objects = UserManager()

    def get_cached_properties(self):
        return [
            'group_values'
        ]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return self.profile.get_absolute_url()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.get_first_name(), self.get_last_name())
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.get_first_name()

    def get_first_name(self):
        return self.memberprofile.first_name

    def get_last_name(self):
        return self.memberprofile.last_name

    def get_profile(self):
        return self.memberprofile

    @cached_property
    def profile(self):
        """Cached version of get_profile"""
        return self.get_profile()

    @cached_property
    def is_email_confirmed(self):
        return EmailAddress.objects.get_primary(self).verified

    @object_cached_property
    def group_values(self):
        return list(Group.objects.filter(user=self).values())

    def profile_image_url(self, size=70, blank=settings.CLUB['gravatar_default']):
        warnings.warn("Stop using user.profile_image_url. Use profile avatar properties.", DeprecationWarning,
                      stacklevel=2)

        fb_uid = SocialAccount.objects.filter(user_id=self.pk, provider='facebook')

        if len(fb_uid):
            return "https://graph.facebook.com/{0}/picture?width={1}&height={2}" \
                .format(fb_uid[0].uid, size, size)

        return "https://www.gravatar.com/avatar/{0}?s={1}&d={2}".format(
            hashlib.md5(self.email).hexdigest(), size, blank)

    def __unicode__(self):
        return self.get_full_name()
