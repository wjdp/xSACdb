

import reversion

from xsd_frontend.activity import DoAction
from xsd_training.models import PerformedQualification


class MemberProfileQualificationMixin:
    @property
    def qualifications_detail(self):
        """Allows quick access to the junction model"""
        return PerformedQualification.objects.filter(trainee=self).select_related('qualification', 'signed_off_by')

    def award_qualification(self, performed_qualification, actor=None):
        """
        Award a qualification to a member, the 'proper' way of doing it
        :param performed_qualification: A prepared PQ instance, you don't need to set trainee.
        :param actor: The officer doing the awarding, NOT the signatory.
        """
        performed_qualification.trainee = self

        with DoAction() as action, reversion.create_revision():
            performed_qualification.save()
            reversion.revisions.set_user(actor)
            action.set(actor=actor, verb='added qualification', action_object=performed_qualification.qualification,
                       target=self, style='qualification-awarded')

    def set_qualification(self, qualification, notes='Created with set_qualification'):
        """
        Quick 'n dirty seting of qualification, no extra fields, no activity actions.
        :param qualification: Qualification instance, NOT PQ
        :param notes: Optionally set a note on the PQ of why you did this rather than using award_qualification
        """
        PerformedQualification(trainee=self, qualification=qualification, mode='OTH', notes=notes).save()
