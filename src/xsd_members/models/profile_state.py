import reversion
from actstream import action
from django.db import transaction


class MemberProfileStateMixin(object):
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
                action.send(actor, verb='approved', target=self, style='mp-approve')
            self.new_notify = False
            self.save()

    def archive(self, actor=None):
        """Archive the user, hiding them from most views and removing a lot of personal data."""
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Archived member')
            if actor:
                action.send(actor, verb='archived', target=self, style='mp-archive')
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
                action.send(actor, verb='restored', target=self, style='mp-restore')
            self.archived = False
            self.save()

    def save(self, *args, **kwargs):
        """Saves changes to the model instance"""
        if self.pk:
            self.cache_update()
        if self.pk and self.user:
            self.sync()

        super(MemberProfileStateMixin, self).save(*args, **kwargs)

    def delete(self):
        # When MP is deleted, we should also remove the user attached to it.
        # Soon we will 'archive' profiles, rather than deleting them.
        user = self.user
        super(MemberProfileStateMixin, self).delete()
        user.delete()
