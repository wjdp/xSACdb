from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView

from xSACdb.ui import xsdUI

from xsd_training.models import *
import forms
from django.forms.models import modelformset_factory    


from xsd_members.bulk_select import get_bulk_members

def overview(request):
    p=request.user.get_profile()
    ui=xsdUI
    ui.app='training'
    ui.page='my_overview'
    ui.section='my'

    return render(request,'overview.html', {
            'ui':ui     
            }, context_instance=RequestContext(request))

def lessons(request):
    p=request.user.get_profile()
    ui=xsdUI
    ui.app='training'
    ui.page='my_lessons'
    ui.section='my'

    return render(request,'lessons.html', {
            'ui':ui     
            }, context_instance=RequestContext(request))

def qualification_detail(request, id):
    qual=Qualification.objects.get(id=id)
    pass

def lesson_detail(request, id):
    lesson=get_object_or_404(Lesson, id=id)
    ui=xsdUI
    ui.app='training'
    ui.page='my_lessons'
    ui.section='my'
    try:
        pl=PerformedLesson.objects.get(trainee=request.user, lesson=lesson)
    except PerformedLesson.DoesNotExist: pl=None
    return render(request, 'lesson_detail.html', {
        'lesson':lesson,
        'pl': pl,
        'ui':ui,
        }, context_instance=RequestContext(request))

def all_feedback(request):
    ui=xsdUI
    ui.app='training'
    ui.section='my'
    ui.page='my_feedback'
    pls=PerformedLesson.objects.filter(trainee=request.user)
    pls=pls.exclude(public_notes="").order_by('-date')

    return render(request,'all_feedback.html', {
                  'ui':ui,
                  'pls':pls
                  }, context_instance=RequestContext(request))

def sdc_list(request,id):
    pass
def sdc_detail(request,id):
    pass

class SessionCreate(CreateView):
    model=Session
    fields=['when','where','notes']
    template_name='session_create.html'

class SessionPlanner(UpdateView):
    model=Session
    fields=['when']
    template_name='session_edit.html'

    def pl_formset(self):
        SessionPlannerTraineeFormSet = modelformset_factory(
            PerformedLesson, fields=['lesson', 'instructor'],
            extra=0
        )
        formset=SessionPlannerTraineeFormSet(
            queryset=PerformedLesson.objects.filter(session=self.object),
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
        pl_formset=self.pl_formset()
        formset=pl_formset(request.POST)
        if formset.is_valid():
            formset.save()
        return super(SessionPlanner, self).post(request, *args, **kwargs)



