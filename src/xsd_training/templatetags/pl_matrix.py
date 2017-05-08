from __future__ import unicode_literals

from django import template

from xsd_training.models import *

register = template.Library()


@register.inclusion_tag('xsd_training/components/pl_matrix.html')
def pl_matrix(trainee):
    if trainee.training_for:
        return {
            'trainee': trainee,
            'modes': Lesson.objects.by_qualification_detailed(trainee.training_for)
        }
    else:
        return {}


@register.inclusion_tag('xsd_training/components/pl_detail.html')
def pl_detail(trainee, lesson):
    context = {
        'trainee': trainee,
        'lesson': lesson,
        'state': lesson.get_lesson_state(trainee),
    }

    try:
        context['pl_latest'] = lesson.get_pls(trainee).select_related('session', 'session__where',
                                                                      'instructor').latest()
    except PerformedLesson.DoesNotExist:
        pass

    return context
