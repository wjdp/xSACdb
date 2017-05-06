from __future__ import unicode_literals

import reversion

from xsd_frontend.activity import DoAction
from xsd_training.models import PerformedQualification


class MemberProfileQualificationMixin(object):
    def award_qualification(self, performed_qualification, actor=None):
        performed_qualification.trainee = self

        with DoAction() as action, reversion.create_revision():
            performed_qualification.save()
            reversion.revisions.set_user(actor)
            action.set(actor=actor, verb='added qualification', target=self, style='qualification-awarded')

    def set_qualification(self, qualification, notes='Created with set_qualification'):
        PerformedQualification(trainee=self, qualification=qualification, mode='OTH', notes=notes).save()
