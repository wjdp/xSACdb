from django import template

from xsd_training.models import *

register = template.Library()

def build_lesson_row(lessons, user):
    lesson_row = ""
    for lesson in lessons:
        pls = PerformedLesson.objects.filter(lesson = lesson, trainee = user)
        if lesson.qualification != user.memberprofile.training_for:
            continue
        completed = False
        partially_completed = False
        mode = lesson.mode
        for pl in pls:
            if pl.completed: completed = True
            if pl.partially_completed: partially_completed = True
        if lesson.code: code_o = lesson.code
        else: code_o = lesson.title
        if completed:                lesson_row += '<td class="completed">'+code_o+'</td>' 
        elif partially_completed:    lesson_row += '<td class="partially_completed">'+code_o+'</td>'
        else:                        lesson_row += '<td class="nothing">'+code_o+'</td>'
    if lesson_row == "": return ""
    else: return "<tr><th>" + mode + "</th>" + lesson_row + "</tr>"



@register.simple_tag
def show_lessons(user, only_main_three=False):
    training_for = user.memberprofile.training_for
    
    lessons = {}

    for mode in Lesson.MODE_CHOICES:
        lessons[mode[0]] = Lesson.objects.filter(mode=mode[0]).order_by('order')

    output = '<table class=" progress-table">\n'
    print lessons
    for mode in Lesson.MODE_CHOICES:
        output += build_lesson_row(lessons[mode[0]], user)

    output += "</table>"

    return output

