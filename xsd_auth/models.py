import base64

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password):
        new_user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = base64.b64encode(email)
        )
        new_user.set_password(password)
        return new_user

class User(AbstractUser):
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
        return self.first_name()

    def get_first_name(self):
        return self.memberprofile.first_name
    def get_last_name(self):
        return self.memberprofile.last_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        return self.memberprofile

    def __unicode__(self):
        return self.get_full_name()
