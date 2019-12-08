

from django import template

from xsd_training.models import *

register = template.Library()


@register.inclusion_tag('xsd_training/components/pl_matrix.html')
def pl_matrix(trainee, qual=None):
    if qual is not None:
        return {
            'trainee': trainee,
            'modes': Lesson.objects.by_qualification_detailed(qual)
        }
    elif trainee.training_for:
        return {
            'trainee': trainee,
            'modes': Lesson.objects.by_qualification_detailed(trainee.training_for)
        }
    else:
        return {}


@register.inclusion_tag('xsd_training/components/pl_history.html')
def pl_history(trainee):
    quals = trainee.qualifications.filter(instructor_qualification=False)
    if quals.count():
        return {
            'trainee': trainee,
            'quals': quals
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
