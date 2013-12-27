from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.core.urlresolvers import reverse_lazy

from xSACdb.roles.decorators import require_training_officer
from xSACdb.roles.mixins import RequireTrainingOfficer

from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table

from django.forms.models import modelformset_factory    

from xsd_members.bulk_select import get_bulk_members

class SessionCreate(RequireTrainingOfficer, CreateView):
    model=Session
    form_class=SessionCreateForm
    template_name='session_create.html'

class SessionPlanner(RequireTrainingOfficer, UpdateView):
    model=Session
    fields=['when']
    template_name='session_edit.html'

    def pl_formset(self, bare=False):
        SessionPlannerTraineeFormSet = modelformset_factory(
            PerformedLesson, form=SessionPLMapForm,
            extra=0
        )
        if bare==True: return SessionPlannerTraineeFormSet
        formset=SessionPlannerTraineeFormSet(
            queryset=PerformedLesson.objects
                .filter(session=self.object)
        )
        return formset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SessionPlanner, self).get_context_data(**kwargs)
        # Add our own custom context
        context['performed_lessons_formset'] = self.pl_formset()
        return context

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        if 'names' in request.GET:
            self.add_trainees(request)
        return super(SessionPlanner, self).get(request, *args, **kwargs)

    def add_trainees(self, request):
        members=get_bulk_members(request)
        for member in members:
            check = PerformedLesson.objects.filter(session=self.object).filter(trainee=member.user)
            if check.count()==0:
                pl=PerformedLesson()
                pl.session=self.object
                pl.trainee=member.user
                pl.save()

    def post(self, request, *args, **kwargs):
        print request.POST
        self.object = self.get_object()
        pl_formset=self.pl_formset(bare=True)
        if request.POST['form-TOTAL_FORMS']!=0:
            formset=pl_formset(request.POST)
            if formset.is_valid():
                formset.save()
        return super(SessionPlanner, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('SessionList')+'?last='+self.kwargs['pk']

class SessionList(RequireTrainingOfficer, ListView):
    model=Session
    template_name='session_list.html'
    context_object_name='sessions'

    def get_context_data(self, **kwargs):
        context = super(SessionList, self).get_context_data(**kwargs)
        if 'last' in self.request.GET:
            context['last'] = int(self.request.GET['last'])
        else:
            context['last'] = 0
        return context

class SessionDelete(RequireTrainingOfficer, DeleteView):
    model=Session
    template_name='session_confirm_delete.html'
    success_url = reverse_lazy('SessionList')


    def get_context_data(self, **kwargs):
        context = super(SessionDelete, self).get_context_data(**kwargs)
        context['pls'] = PerformedLesson.objects.filter(session=self.object)
        return context