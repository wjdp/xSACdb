from django import template
register = template.Library()

@register.inclusion_tag('xsd_training/lesson_list_template.html')
def show_lessons(qualification, mode, user):
    lessons=qualification.lessons_by_mode(mode=mode)
    
    completed=[]
    uncompleted=[]

    for lesson in lessons:
        if lesson.is_completed(user):
            completed.append(lesson)
        else:
            uncompleted.append(lesson)

    return {'lessons':uncompleted,'completed':completed,}

from xsd_training.models import PerformedLesson

@register.inclusion_tag('xsd_training/lesson_list_template.html')
def show_upcoming_lessons(user):
    pl_upcoming=PerformedLesson.objects.filter(trainee=user, completed=False)

    lessons=[]

    for pl in pl_upcoming:
        lessons.append(pl.lesson)

    return {'lessons':lessons,'completed':None,}
