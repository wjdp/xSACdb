

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from xSACdb.roles.decorators import require_instructor, require_training_officer
from xSACdb.roles.mixins import RequireInstructor
from xSACdb.views import OrderedListView
from xsd_training.forms import *


@require_instructor
def InstructorUpcoming(request):
    def get_upcoming_sessions_by_instructor(instructor):
        now = datetime.datetime.now() - Session.LESSON_HISTORY
        sessions_query = Session.objects.filter(when__gte=now).order_by('when')

        sessions = []

        for session in sessions_query:
            pls = PerformedLesson.objects.filter(session=session)
            involved = False
            pls_teaching = []
            for pl in pls:
                if pl.instructor == instructor:
                    involved = True
                    pls_teaching.append(pl)
            if involved:
                sessions.append((session, pls_teaching))
        return sessions

    instructor = request.user.memberprofile
    upcoming_sessions = get_upcoming_sessions_by_instructor(instructor)

    return render(request, 'instructor_upcoming.html', {
        'upcoming_sessions': upcoming_sessions
    })


class TraineeNotesSearch(RequireInstructor, OrderedListView):
    model = MemberProfile
    template_name = 'xsd_training/trainee/search.html'
    context_object_name = 'trainees'
    order_by = 'last_name'

    def get_queryset(self):
        queryset = super(TraineeNotesSearch, self).get_queryset()
        if 'q' in self.request.GET:
            name = self.request.GET['q']
            queryset = queryset.filter(
                Q(last_name__icontains=name) |
                Q(first_name__icontains=name)
            )
        queryset = queryset.prefetch_related(
            'top_qual_cached',
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TraineeNotesSearch, self).get_context_data()
        if 'q' in self.request.GET:
            context['q'] = self.request.GET['q']
        return context


class TraineeNotes(RequireInstructor, DetailView):
    model = MemberProfile
    template_name = 'xsd_training/trainee/detail.html'
    context_object_name = 'trainee'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TraineeNotes, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['trainee'] = self.get_object().memberprofile
        pls = PerformedLesson.objects.filter(trainee=self.get_object())
        context['pls'] = pls
        context['planned'] = pls.filter(completed=False, partially_completed=False).count()
        context['partially_completed'] = pls.filter(completed=False, partially_completed=True).count()
        context['completed'] = pls.filter(completed=True, partially_completed=False).count()

        # Forms for trainee updation
        context['current_qual_form'] = MiniQualificationSetForm()
        context['training_for_form'] = MiniTrainingForSetForm(self.get_object())
        context['instructor_form'] = MiniInstructorQualificationSetForm()
        context['sdc_form'] = MiniTraineeSDCAddForm()

        # Forms for modals
        return context


@require_training_officer
def trainee_notes_set(request, pk):
    if 'field' in request.GET:
        trainee_profile = get_object_or_404(MemberProfile, pk=pk)
        if request.GET['field'] == 'training_for':
            if request.GET['qualification'] == "":
                # Remove
                trainee_profile.training_for = None
            else:
                q = get_object_or_404(Qualification, pk=request.GET['qualification'])
                trainee_profile.training_for = q
            trainee_profile.save()
        if request.GET['field'] == 'sdc':
            sdc = get_object_or_404(SDC, pk=request.GET['sdc'])
            trainee_profile.add_sdc(sdc)
            trainee_profile.save()
        if request.GET['field'] == 'remove_sdc':
            sdc = get_object_or_404(SDC, pk=request.GET['sdc'])
            trainee_profile.sdcs.remove(sdc)
            trainee_profile.save()

        return redirect(reverse('xsd_training:TraineeNotes', kwargs={'pk': pk}))
    else:
        return HttpResponse('No field specified')
