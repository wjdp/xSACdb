from django import template
register = template.Library()

@register.inclusion_tag('lesson_list_template.html')
def show_lessons(qualification, mode, user):
    lessons=qualification.lessons_by_mode(mode=mode)
    
    completed=[]
    planned=[]
    uncompleted=[]

    for lesson in lessons:
        if lesson.is_completed(user):
            completed.append(lesson)
        elif lesson.is_planned(user):
            planned.append(lesson)
        else:
            uncompleted.append(lesson)

    return {'lessons':uncompleted,'completed':completed,'planned':planned,}

from xsd_training.models import PerformedLesson

@register.inclusion_tag('lesson_list_template.html')
def show_upcoming_lessons(user):
    pl_upcoming=PerformedLesson.objects.filter(trainee=user, completed=False)

    lessons=[]

    for pl in pl_upcoming:
        lessons.append(pl.lesson)

    return {'lessons':lessons,'completed':None,}
