from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from xsd_training.models import *

def overview(request):
    p=request.user.get_profile()

    theory=p.training_for.lessons_by_mode(mode='TH')
    sheltered=p.training_for.lessons_by_mode(mode='SH')
    open_water=p.training_for.lessons_by_mode(mode='OW')
    dry_practical=p.training_for.lessons_by_mode(mode='DP')

    experience=p.training_for.lessons_by_mode(mode='XP')

    return render(request,'xsd_training/overview.html', {
               'lessons_theory':theory,
               'lessons_sheltered':sheltered,
               'lessons_open_water':open_water,
               'lessons_dry_practical':dry_practical,
               'experience':experience,
    
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

def sdc_list(request,id):
    pass
def sdc_detail(request,id):
    pass
