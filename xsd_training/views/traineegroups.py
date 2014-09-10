from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse_lazy

from xSACdb.roles.decorators import require_training_officer
from xSACdb.roles.mixins import RequireTrainingOfficer

from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table

from xsd_members.bulk_select import get_bulk_members

class TraineeGroupList(RequireTrainingOfficer,ListView):
    model=TraineeGroup
    template_name='traineegroup_list.html'
    context_object_name='tgs'

class TraineeGroupCreate(RequireTrainingOfficer,CreateView):
    model=TraineeGroup
    template_name='traineegroup_create.html'
    success_url = reverse_lazy('TraineeGroupList')

class TraineeGroupUpdate(RequireTrainingOfficer,DetailView):
    model=TraineeGroup
    template_name='traineegroup_update.html'
    context_object_name='tg'
    success_url = reverse_lazy('TraineeGroupList')

    def get_context_data(self, **kwargs):
        context = super(TraineeGroupUpdate, self).get_context_data(**kwargs)
        context['trainees'] = context['tg'].trainees.all() 
        return context

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        trainee_table.remove_trainee(request, self.object)
        if 'names' in request.GET:
            self.add_trainees(request)
        return super(TraineeGroupUpdate, self).get(request, *args, **kwargs)

    def add_trainees(self, request):
        members=get_bulk_members(request)
        for member in members:
            if member.user not in self.object.trainees.all():
                self.object.trainees.add(member.user)
        self.object.save()

class TraineeGroupDelete(RequireTrainingOfficer,DeleteView):
    model=TraineeGroup
    template_name='traineegroup_delete.html'
    context_object_name='tg'
    success_url = reverse_lazy('TraineeGroupList')

class TraineeGroupProgress(RequireTrainingOfficer, TraineeGroupList):
    template_name='traineegroup_progress.html'
    def get_context_data(self, **kwargs):
        context = super(TraineeGroupProgress, self).get_context_data(**kwargs)
        if 'tg' in self.request.GET:
            context['tg'] = TraineeGroup.objects.get(pk=self.request.GET['tg'])
        return context