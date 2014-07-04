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

@register.inclusion_tag('lesson_list_template_with_dates.html')
def show_upcoming_lessons(user):
    pl_upcoming=PerformedLesson.objects.filter(trainee=user, completed=False, partially_completed=False).order_by('date')

    lessons=[]

    for pl in pl_upcoming:
        lessons.append((pl.lesson,pl))

    return {'planned':lessons,'completed':None,}

@register.filter
def has_sdc(user,sdc):
    if sdc in user.get_profile().sdcs.all(): return True
    else: return False

@register.filter
def has_sdc_interest(user,sdc):
    if user in sdc.interested_members.all(): return True
    else: return False

@register.filter
def cando_sdc(profile,sdc):
    if profile.top_qual()==None: my_rank=0
    else: my_rank=profile.top_qual().rank
    if sdc.min_qualification==None: sdc_rank=0
    else: sdc_rank=sdc.min_qualification.rank
    if my_rank>=sdc_rank:
        return True
    else: return False