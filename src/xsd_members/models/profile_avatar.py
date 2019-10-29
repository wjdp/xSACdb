

import hashlib

from allauth.socialaccount.models import SocialAccount
from django.conf import settings

from xSACdb.cache import object_cached_property


class MemberProfileAvatarMixin(object):
    def get_cached_properties(self):
        cps = super(MemberProfileAvatarMixin, self).get_cached_properties()
        cps += [
            'avatar_xs',
            'avatar_sm',
            'avatar_md',
        ]
        return cps

    def get_avatar(self, size=70, blank=settings.CLUB['gravatar_default']):
        if self.user:
            fb_uid = SocialAccount.objects.filter(user_id=self.user.pk, provider='facebook')

            if len(fb_uid):
                return "https://graph.facebook.com/{0}/picture?width={1}&height={2}" \
                    .format(fb_uid[0].uid, size, size)

        return "https://www.gravatar.com/avatar/{0}?s={1}&d={2}".format(
            hashlib.md5(self.email).hexdigest(), size, 'retro')

    @object_cached_property
    def avatar_xs(self):
        if self.user:
            return self.get_avatar(size=32)
        else:
            return None

    @object_cached_property
    def avatar_sm(self):
        if self.user:
            return self.get_avatar(size=64)
        else:
            return None

    @object_cached_property
    def avatar_md(self):
        if self.user:
            return self.get_avatar(size=128)
        else:
            return None
