# TODO Depreciate

from django import template

register = template.Library()

def ret_active_if_equal(parser,token):
    try:
        tag_name, iff, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments (if and value)" % token.contents.split()[0])
    if not (value[0] == value[-1] and value[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    
    return RetActiveNode(iff,value[1:-1])


class RetActiveNode(template.Node):
    active=False
    def __init__(self, iff, value):
        if iff==value: active=False
    def render(self, context):
        if active: return "class='active'"
        else: return None

register.tag('is_active', ret_active_if_equal)

@register.simple_tag
def is_active_simple(iff,value):
    if iff==value: return "class='active'"
    else: return None
