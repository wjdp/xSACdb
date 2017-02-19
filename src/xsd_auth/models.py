from __future__ import unicode_literals

import random
import hashlib

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DJ_UserManager
from django.utils.functional import cached_property


class UserManager(DJ_UserManager):
    # FIXME either match signature of UserManager / switch to allauth managed
    def create_user(self, first_name, last_name, email, password):
        new_user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=random.randrange(1000000000000000,9999999999999999)
        )
        new_user.set_password(password)
        return new_user

from actstream.actions import follow, unfollow

class UserActivityMixin(object):
    def follow_defaults(self):
        follow(self, self.profile, actor_only=False)


class User(UserActivityMixin, AbstractUser):
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

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

    def profile_image_url(self, size=70):
        fb_uid = SocialAccount.objects.filter(user_id=self.pk, provider='facebook')

        if len(fb_uid):
            return "https://graph.facebook.com/{}/picture?width={}&height={}" \
                .format(fb_uid[0].uid, size, size)

        return "https://www.gravatar.com/avatar/{}?s={}".format(
            hashlib.md5(self.email).hexdigest(), size)

    def __unicode__(self):
        return self.get_full_name()
