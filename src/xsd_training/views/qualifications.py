

from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireTrainingOfficer
from xsd_training.forms import *
from xsd_training.views.base import TraineeFormMixin


class QualificationFormMixin(TraineeFormMixin):
    def get_success_url(self):
        return '{}#qualification-list'.format(
            reverse('xsd_training:TraineeNotes', kwargs={'pk': self.kwargs['t_pk']}))


class QualificationCreate(RequireTrainingOfficer, QualificationFormMixin, CreateView):
    model = PerformedQualification
    form_class = PerformedQualificationForm
    template_name = 'xsd_training/trainee/qualification_form.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.get_trainee().award_qualification(self.object, actor=self.request.user)

        messages.add_message(self.request, messages.SUCCESS,
                             '{} awarded to {}'.format(self.object.qualification, self.get_trainee().full_name))

        return super(QualificationCreate, self).form_valid(form)


class QualificationUpdate(RequireTrainingOfficer, QualificationFormMixin, UpdateView):
    model = PerformedQualification
    fields = ['mode', 'xo_from', 'signed_off_on', 'signed_off_by', 'notes', ]
    template_name = 'xsd_training/trainee/qualification_form.html'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
                             '{} updated on {}'.format(self.get_object().qualification, self.get_trainee().full_name))
        return super(QualificationUpdate, self).form_valid(form)


class QualificationDelete(RequireTrainingOfficer, QualificationFormMixin, DeleteView):
    model = PerformedQualification

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             '{} removed from {}'.format(self.get_object().qualification, self.get_trainee().full_name))
        return super(QualificationDelete, self).delete(request, args, kwargs)
