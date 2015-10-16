from django import template
register = template.Library()

@register.inclusion_tag('lesson_list_template.html')
def show_lessons(qualification, mode, mp):
    lessons=qualification.lessons_by_mode(mode=mode)

    completed=[]
    planned=[]
    partially_completed=[]
    uncompleted=[]

    for lesson in lessons:
        if lesson.is_completed(mp):
            completed.append(lesson)
        elif lesson.is_planned(mp):
            planned.append(lesson)
        elif lesson.is_partially_completed(mp):
            partially_completed.append(lesson)
        else:
            uncompleted.append(lesson)

    return {'lessons':uncompleted,'completed':completed,'planned':planned, 'partially_completed':'partially_completed'}

from xsd_training.models import PerformedLesson

@register.inclusion_tag('lesson_list_template_with_dates.html')
def show_upcoming_lessons(mp):
    pl_upcoming=PerformedLesson.objects.get_lessons(trainee=mp, completed=False, partially_completed=False).order_by('date')

    lessons=[]

    for pl in pl_upcoming:
        lessons.append((pl.lesson,pl))

    return {'planned':lessons,'completed':None,}

@register.filter
def has_sdc(mp,sdc):
    if sdc in mp.sdcs.all(): return True
    else: return False

@register.filter
def has_sdc_interest(mp,sdc):
    if mp in sdc.interested_members.all(): return True
    else: return False

@register.filter
def cando_sdc(profile, sdc):
    if profile.top_qual()==None: my_rank=0
    else: my_rank=profile.top_qual().rank
    if sdc.min_qualification==None: sdc_rank=0
    else: sdc_rank=sdc.min_qualification.rank
    if my_rank>=sdc_rank:
        return True
    else: return False
