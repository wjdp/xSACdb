from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from xSACdb.ui import xsdUI
from xSACdb.roles.decorators import require_verified

from xsd_training.models import *
from xsd_training.forms import *

@require_verified
def overview(request):
    ui=xsdUI
    ui.app='training'
    ui.page='my_overview'
    ui.section='my'

    quals = Qualification.objects.filter(instructor_qualification=False)

    return render(request,'overview.html', {
            'ui':ui,
            'quals':quals,     
            }, context_instance=RequestContext(request))

@require_verified
def lessons(request):
    ui=xsdUI
    ui.app='training'
    ui.page='my_lessons'
    ui.section='my'

    return render(request,'lessons.html', {
            'ui':ui     
            }, context_instance=RequestContext(request))

@require_verified
def lesson_detail(request, id):
    lesson=get_object_or_404(Lesson, id=id)
    ui=xsdUI
    ui.app='training'
    ui.page='my_lessons'
    ui.section='my'
    try:
        pls=PerformedLesson.objects.filter(trainee=request.user, lesson=lesson).order_by('date')
    except PerformedLesson.DoesNotExist: pl=None
    return render(request, 'lesson_detail.html', {
        'lesson':lesson,
        'pls': pls,
        'ui':ui,
        }, context_instance=RequestContext(request))

@require_verified
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