from __future__ import unicode_literals

import reversion

from xSACdb.middleware import NewbieProfileFormRedirectMiddleware
from xsd_frontend.activity import DoAction


class MemberProfileStateMixin(object):
    @property
    def verified(self):
        return not self.new_notify

    def approve(self, actor=None, bare=False):
        """
        Set whatever property we need to approve this member.
        """

        def _approve():
            self.new_notify = False
            self.save()

        if bare:
            _approve()
        elif actor is not None:
            with DoAction() as action, reversion.create_revision():
                if actor:
                    action.set(actor=actor, verb='approved', target=self, style='mp-approve')
                _approve()
        else:
            raise ValueError('You must specify actor or set bare')

    def archive(self, actor=None, bare=False):
        """Archive the user, hiding them from most views and removing a lot of personal data."""

        def _archive():
            self.expunge()
            self.archived = True
            self.save()
            # This middleware controls access to site dependant on missing fields
            NewbieProfileFormRedirectMiddleware.invalidate_cache(self.user)

        if bare:
            _archive()
        elif actor is not None:
            with DoAction() as action, reversion.create_revision():
                if actor:
                    action.set(actor=actor, verb='archived', target=self, style='mp-archive')
                _archive()
        else:
            raise ValueError('You must specify actor or set bare')

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

    def reinstate(self, actor=None, bare=False):
        """Opposite of archive"""

        def _reinstate():
            self.archived = False
            self.save()

        if bare:
            _reinstate()
        elif actor is not None:
            with DoAction() as action, reversion.create_revision():
                if actor:
                    action.set(actor=actor, verb='restored', target=self, style='mp-restore')
                _reinstate()
        else:
            raise ValueError('You must specify actor or set bare')

    def save(self, *args, **kwargs):
        """Saves changes to the model instance"""
        if self.pk and self.user:
            self.sync()

        super(MemberProfileStateMixin, self).save(*args, **kwargs)

    def delete(self):
        # When MP is deleted, we should also remove the user attached to it.
        # Soon we will 'archive' profiles, rather than deleting them.
        user = self.user
        super(MemberProfileStateMixin, self).delete()
        user.delete()
