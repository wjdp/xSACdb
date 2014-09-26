from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from django.shortcuts import redirect, render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

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
    fields=['when', 'where', 'notes']
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
        context['traineegroup_select'] = TraineeGroupSelectForm()
        return context

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        if 'names' in request.GET:
            self.add_trainees(request)
        if 'traineegroup' in request.GET:
            self.add_trainee_group(request.GET['traineegroup'])
        if 'remove-trainee' in request.GET:
            self.remove_trainee(request.GET['remove-trainee'])
        return super(SessionPlanner, self).get(request, *args, **kwargs)

    def add_trainees(self, request):
        members=get_bulk_members(request)
        for member in members:
            check = PerformedLesson.objects.filter(session=self.object).filter(trainee=member.user)
            if not check.exists():
                pl=PerformedLesson()
                pl.session=self.object
                pl.trainee=member.user
                pl.save()

    def add_trainee_group(self, group):
        tg=get_object_or_404(TraineeGroup, pk=group)
        for user in tg.trainees.all():
            check = PerformedLesson.objects.filter(session=self.object).filter(trainee=user)
            if not check.exists():
                pl=PerformedLesson()
                pl.session=self.object
                pl.trainee=user
                pl.save()

    def remove_trainee(self, trainee_pk):
        trainee=get_object_or_404(User, pk=trainee_pk)
        pl=get_object_or_404(PerformedLesson, session=self.object, trainee=trainee)
        pl.delete()

    def post(self, request, *args, **kwargs):
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

    def get_queryset(self):
        qs = super(SessionList, self).get_queryset().order_by('when').exclude(completed=True)
        return qs

class SessionComplete(RequireTrainingOfficer,DetailView):
    model=Session
    template_name='session_complete.html'
    context_object_name='session'

    def build_pls_formset(self, bare=False):
        SessionCompleteFormSet = modelformset_factory(
            PerformedLesson, form=SessionCompleteForm,
            extra=0
        )
        if not bare:
            formset=SessionCompleteFormSet(
                queryset=PerformedLesson.objects
                    .filter(session=self.object)
            )
        else:
            formset = SessionCompleteFormSet
        return formset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SessionComplete, self).get_context_data(**kwargs)
        # Add our own custom context
        context['performed_lessons_formset'] = self.build_pls_formset()
        return context

    def get_users(self,request):
        users=[]
        for item in request.POST:
            if re.match('user',item):
                user_pk=item[5:]
                u=User.objects.get(pk=user_pk)
                users.append(u)
        return users

    def set_pl(self, id, completed, partially_completed, public_notes, private_notes):
        pl = id
        if not completed and not partially_completed:
            # This will be a no-show, so delete the PL
            pl.delete()
        else:
            if completed and partially_completed:
                completed = False # Mark as not completed if partially is ticked

            # Stick data in object
            pl.completed = completed
            pl.partially_completed = partially_completed
            pl.public_notes = public_notes
            pl.private_notes = private_notes
            # And save it
            pl.save()

    def set_pl_save(self, id, completed, partially_completed, public_notes, private_notes):
        pl = id
        if completed and partially_completed:
            completed = False # Mark as not completed if partially is ticked

        # Stick data in object
        pl.completed = completed
        pl.partially_completed = partially_completed
        pl.public_notes = public_notes
        pl.private_notes = private_notes
        # And save it
        pl.save()

    def post(self, request, *args, **kwargs):
            SessionCompleteFormSet = self.build_pls_formset(True) 
            formset = SessionCompleteFormSet(request.POST)
            if formset.is_valid():
                if 'complete' in request.POST:
                    for form in formset.cleaned_data:
                        self.set_pl(form['id'], form['completed'], form['partially_completed'], form['public_notes'], form['private_notes'])
                    this_session = self.get_object()
                    this_session.completed = True
                    this_session.save()
                else:
                    for form in formset.cleaned_data:
                        self.set_pl_save(form['id'], form['completed'], form['partially_completed'], form['public_notes'], form['private_notes'])
                    return self.get(request, *args, **kwargs)
                return redirect(reverse_lazy('SessionList'))
            else:
                return self.get(request, *args, **kwargs)

class SessionDelete(RequireTrainingOfficer, DeleteView):
    model=Session
    template_name='session_confirm_delete.html'
    success_url = reverse_lazy('SessionList')

    def get_context_data(self, **kwargs):
        context = super(SessionDelete, self).get_context_data(**kwargs)
        context['pls'] = PerformedLesson.objects.filter(session=self.object)
        return context

@require_training_officer
def pool_sheet(request):
    if request.GET:
        form = PoolSheetOptions(request.GET)
        if form.is_valid():
            return pool_sheet_generate(request, form)
    else:
        form = PoolSheetOptions()

    return render(request, 'pool_sheet.html', {'form':form})

@require_training_officer
def pool_sheet_generate(request, form):
    session = form.cleaned_data['session']
    pls = PerformedLesson.objects.filter(session = session)
    
    pls_extended = []

    number_of_notes = form.cleaned_data['number_of_notes']
    for pl in pls:
        recent_pls = PerformedLesson.objects.filter(trainee = pl.trainee, lesson__mode = pl.lesson.mode, completed=True).order_by('date')[:number_of_notes]
        notes = []
        for rpl in recent_pls:
            if rpl.public_notes or rpl.private_notes: notes.append(rpl)
        pls_extended.append((pl, notes))

    
    return render(request, 'pool_sheet_generate.html', {
        'session': session,
        'pls_extended': pls_extended,
        'show_public_notes': form.cleaned_data['show_public_notes'],
        'show_private_notes': form.cleaned_data['show_private_notes'],
        'comments_column': form.cleaned_data['comments_column'],
        'signature_column': form.cleaned_data['signature_column'],
        })