

from django.shortcuts import render

from xSACdb.roles.decorators import require_verified
from xSACdb.ui import xsdUI
from xsd_training.forms import *


@require_verified
def overview(request):
    ui = xsdUI
    ui.app = 'training'
    ui.page = 'my_overview'
    ui.section = 'my'

    quals = Qualification.objects.get_active(trainee=request.user.memberprofile).filter(instructor_qualification=False)

    return render(request, 'overview.html', {
        'ui': ui,
        'quals': quals,
    })


@require_verified
def lessons(request):
    ui = xsdUI
    ui.app = 'training'
    ui.page = 'my_lessons'
    ui.section = 'my'

    return render(request, 'lessons.html', {
        'ui': ui
    })


@require_verified
def all_feedback(request):
    ui = xsdUI
    ui.app = 'training'
    ui.section = 'my'
    ui.page = 'my_feedback'
    pls = PerformedLesson.objects.filter(trainee=request.user.memberprofile)
    pls = pls.exclude(public_notes="").order_by('-date')

    return render(request, 'all_feedback.html', {
        'ui': ui,
        'pls': pls
    })
