import base64
import hashlib

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from allauth.socialaccount.models import SocialAccount

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

    bsac_email = models.EmailField(blank=True)
    bsac_password = models.CharField(max_length=128, blank=True)
    # Y: Success, N: Failed, A: Awaiting, N: U & P not set,
    bsac_state = models.CharField(max_length=1, default='N')

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

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        return self.memberprofile

    def profile_image_url(self, size=70):
        fb_uid = SocialAccount.objects.filter(user_id=self.pk, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width={}&height={}"\
                .format(fb_uid[0].uid, size, size)

        return "http://www.gravatar.com/avatar/{}?s={}".format(
            hashlib.md5(self.email).hexdigest(), size)

    def set_bsac_auth(email, password):
        self.bsac_email = email
        self.bsac_password = password
        if email == '':
            self.bsac_state = 'N'
        else:
            self.bsac_state = 'A'
        self.save()

    def __unicode__(self):
        return self.get_full_name()
