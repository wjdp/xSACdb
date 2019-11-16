import commonmark

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def markdown(md, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    html = commonmark.commonmark(esc(md))
    return mark_safe(html)
