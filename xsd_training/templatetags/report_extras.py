from django import template

from xsd_training.models import *

register = template.Library()

def build_lesson_row(lessons, user):
    lesson_row = ""
    for lesson in lessons:
        pls = PerformedLesson.objects.filter(lesson = lesson, trainee = user)
        completed = False
        partially_completed = False
        mode = lesson.mode
        for pl in pls:
            if pl.completed: completed = True
            if pl.partially_completed: partially_completed = True

        if completed:                lesson_row += '<td class="completed">'+lesson.code+'</td>' 
        elif partially_completed:    lesson_row += '<td class="partially_completed">'+lesson.code+'</td>'
        else:                        lesson_row += '<td class="nothing">'+lesson.code+'</td>'

    return "<tr><th>" + mode + "</th>" + lesson_row + "</tr>"



@register.simple_tag
def show_lessons(user):
    training_for = user.memberprofile.training_for
    
    theory_lessons = Lesson.objects.filter(mode='TH').order_by('order')
    sheltered_water_lessons = Lesson.objects.filter(mode='SW').order_by('order')
    open_water_lessons = Lesson.objects.filter(mode='OW').order_by('order')

    output = '<table class=" progress-table">\n'

    output += build_lesson_row(theory_lessons, user)
    output += build_lesson_row(sheltered_water_lessons, user)
    output += build_lesson_row(open_water_lessons, user)

    output += "</table>"

    return output

