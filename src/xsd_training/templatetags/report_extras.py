from __future__ import unicode_literals

from django import template

from xsd_training.models import *

register = template.Library()


def build_lesson_row(lessons, mp):
    lesson_row = ""
    for lesson in lessons:
        pls = PerformedLesson.objects.filter(lesson=lesson, trainee=mp)
        if lesson.qualification != mp.training_for:
            continue
        completed = False
        partially_completed = False
        mode = lesson.mode
        for pl in pls:
            if pl.completed: completed = True
            if pl.partially_completed: partially_completed = True
        if lesson.code:
            code_o = lesson.code
        else:
            code_o = lesson.title
        lesson_row += '<td data-l=' + str(lesson.pk) + " data-t=" + str(mp.pk) + " data-q=" + str(
            lesson.qualification.pk)
        if completed:
            lesson_row += ' class="ljs completed">'
        elif partially_completed:
            lesson_row += ' class="ljs partially_completed">'
        else:
            lesson_row += ' class="ljs nothing">'
        lesson_row += code_o + '</td>'
    if lesson_row == "":
        return ""
    else:
        return "<tr class='mode--{0}'>\n<th>{0}</th>\n{1}\n</tr>".format(mode, lesson_row)


@register.simple_tag
def show_lessons(mp, only_main_three=False):
    training_for = mp.training_for

    lessons = {}

    for mode in Lesson.MODE_CHOICES:
        lessons[mode[0]] = Lesson.objects.filter(mode=mode[0]).order_by('order').prefetch_related('qualification')

    output = '<table class="table table-sm xsd-pl-matrix">\n'
    for mode in Lesson.MODE_CHOICES:
        output += build_lesson_row(lessons[mode[0]], mp)

    output += "</table>"

    return output
