from django import template

register = template.Library()


@register.simple_tag
def is_active_simple(iff,value):
    if iff==value: return "class='active'"
    else: return None
