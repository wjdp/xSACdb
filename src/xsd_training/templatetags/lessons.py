from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

from xsd_training.models import *

register = template.Library()

@register.simple_tag
def pl_state_icon(pl):
    """Output an icon given a PL and it's state"""
    icon = {
        Lesson.LESSON_STATE_PLANNED: 'fa fa-fw fa-calendar-o',
        Lesson.LESSON_STATE_PARTIAL: 'fa fa-fw fa-circle-o',
        Lesson.LESSON_STATE_YES: 'fa fa-fw fa-check',
    }[pl.state]

    return mark_safe("<i class='{icon}'></i>".format(icon=icon))

