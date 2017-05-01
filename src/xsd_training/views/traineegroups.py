from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

import xsd_training.trainee_table as trainee_table
from xSACdb.roles.mixins import RequireTrainingOfficer
from xSACdb.views import ActionView
from xsd_members.bulk_select import get_bulk_members
from xsd_training.forms import *


class TraineeGroupList(RequireTrainingOfficer, ListView):
    model = TraineeGroup
    template_name = 'xsd_training/traineegroup/list.html'
    context_object_name = 'tgs'


class TraineeGroupCreate(RequireTrainingOfficer, SuccessMessageMixin, CreateView):
    model = TraineeGroup
    template_name = 'xsd_training/traineegroup/create.html'
    success_url = reverse_lazy('xsd_training:TraineeGroupList')

    # To fix "Django Using ModelFormMixin (base class of CreateUserView) without the 'fields' attribute is prohibited."
    # See #139 Creating new training groups fails
    fields = '__all__'

    def get_success_message(self, cleaned_data):
        return 'Added trainee group {}'.format(cleaned_data['name'])


class TraineeGroupUpdate(RequireTrainingOfficer, DetailView):
    model = TraineeGroup
    template_name = 'xsd_training/traineegroup/update.html'
    context_object_name = 'tg'
    success_url = reverse_lazy('xsd_training:TraineeGroupList')

    def get_context_data(self, **kwargs):
        context = super(TraineeGroupUpdate, self).get_context_data(**kwargs)
        context['trainees'] = context['tg'].get_all_trainees()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        trainee_table.remove_trainee(request, self.object)

        return super(TraineeGroupUpdate, self).get(request, *args, **kwargs)


class TraineeGroupAction(RequireTrainingOfficer, ActionView):
    model = TraineeGroup

    def add(self, request):
        members = get_bulk_members(request)
        self.get_object().add_trainees(members)

    def remove(self, request):
        members = get_bulk_members(request)
        self.get_object().remove_trainees(members)


class TraineeGroupDelete(RequireTrainingOfficer, DeleteView):
    model = TraineeGroup
    template_name = 'xsd_training/traineegroup/delete.html'
    context_object_name = 'tg'
    success_url = reverse_lazy('xsd_training:TraineeGroupList')


# RequireTrainingOfficer is inherited
class TraineeGroupProgress(TraineeGroupList):
    template_name = 'xsd_training/traineegroup/progress.html'

    def get_context_data(self, **kwargs):
        context = super(TraineeGroupProgress, self).get_context_data(**kwargs)
        if 'tg' in self.request.GET:
            context['tg'] = TraineeGroup.objects.get(pk=self.request.GET['tg'])
        return context
