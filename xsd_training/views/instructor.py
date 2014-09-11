from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import DetailView

from xSACdb.roles.decorators import require_instructor
from xSACdb.roles.mixins import RequireInstructor

from xsd_training.models import *
from xsd_training.forms import *

import datetime

@require_instructor
def InstructorUpcoming(request):
    def get_upcoming_sessions_by_instructor(instructor):
        now=datetime.datetime.now()+datetime.timedelta(days=1)
        sessions_query=Session.objects.filter(when__gt=now).order_by('when')

        sessions=[]

        for session in sessions_query:
            pls=PerformedLesson.objects.filter(session=session)
            involved=False
            pls_teaching=[]
            for pl in pls:
                if pl.instructor==instructor:
                    involved=True
                    pls_teaching.append(pl)
            if involved:
                sessions.append((session,pls_teaching))
        return sessions

    instructor=request.user
    upcoming_sessions=get_upcoming_sessions_by_instructor(instructor)

    return render(request,'instructor_upcoming.html', {
        'upcoming_sessions':upcoming_sessions     
    }, context_instance=RequestContext(request))

@require_instructor
def TraineeNotesSearch(request):
    if 'surname' in request.GET:
        surname=request.GET['surname']
        trainees=User.objects.filter(last_name__contains=surname)
    else: trainees=None

    return render(request, 'trainee_notes_search.html', {
        'trainees':trainees
    }, context_instance=RequestContext(request))

class TraineeNotes(RequireInstructor, DetailView):
    model = User
    template_name = 'trainee_notes.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TraineeNotes, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['trainee']    = self.get_object().memberprofile
        pls        = PerformedLesson.objects.filter(trainee = self.get_object())
        context['pls'] = pls
        context['planned'] = pls.filter(completed = False, partially_completed = False).count()
        context['partially_completed'] = pls.filter(completed = False, partially_completed = True).count()
        context['completed'] = pls.filter(completed = True, partially_completed = False).count()
        return context