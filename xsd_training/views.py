from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from xSACdb.ui import xsdUI

from xsd_training.models import *

def overview(request):
    p=request.user.get_profile()
    ui=xsdUI
    ui.app='training'
    ui.page='my_overview'
    ui.section='my'

    return render(request,'xsd_training/overview.html', {
            'ui':ui     
            }, context_instance=RequestContext(request))

def lessons(request):
    p=request.user.get_profile()
    ui=xsdUI
    ui.app='training'
    ui.page='my_lessons'
    ui.section='my'

    return render(request,'xsd_training/lessons.html', {
            'ui':ui     
            }, context_instance=RequestContext(request))

def qualification_detail(request, id):
    qual=Qualification.objects.get(id=id)
    pass

def lesson_detail(request, id):
    lesson=get_object_or_404(Lesson, id=id)
    try:
        pl=PerformedLesson.objects.get(trainee=request.user, lesson=lesson)
    except PerformedLesson.DoesNotExist: pl=None
    return render(request, 'xsd_training/lesson_detail.html', {
        'lesson':lesson,
        'pl': pl
        }, context_instance=RequestContext(request))

def all_feedback(request):
    ui=xsdUI
    ui.app='training'
    ui.section='my'
    ui.page='my_feedback'
    pls=PerformedLesson.objects.filter(trainee=request.user)
    pls=pls.exclude(public_notes="").order_by('-date')

    return render(request,'xsd_training/all_feedback.html', {
                  'ui':ui,
                  'pls':pls
                  }, context_instance=RequestContext(request))

def sdc_list(request,id):
    pass
def sdc_detail(request,id):
    pass
