from django.db import models

class MemberProfileManager(models.Manager):
    def all(self):
        # Filtering is applied here to hide 'hidden' users
        return super(MemberProfileManager, self).all().exclude(hidden=True)

    def all_actual(self):
        return super(MemberProfileManager, self).all()
