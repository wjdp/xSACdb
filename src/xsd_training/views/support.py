

from django.urls import reverse_lazy

from xSACdb.roles.mixins import RequireTrainingOfficer
from xsd_frontend.base import BaseUpdateRequestList, BaseUpdateRequestRespond


class TrainingUpdateRequestList(RequireTrainingOfficer, BaseUpdateRequestList):
    template_name = "training_update_request.html"
    area = 'tra'
    form_action = reverse_lazy('xsd_training:TrainingUpdateRequestRespond')
    custom_include = 'training_update_request_custom.html'


class TrainingUpdateRequestRespond(RequireTrainingOfficer, BaseUpdateRequestRespond):
    success_url = reverse_lazy('xsd_training:TrainingUpdateRequestList')
