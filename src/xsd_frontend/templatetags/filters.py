

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value*arg

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.simple_tag
def url_replace(request, field, value):
    """Puts a GET parameter into a url?"""
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def order_by(request, field, attr):

    dict_ = request.GET.copy()

    if dict_.__contains__(field) and dict_[field] == attr:
        if not dict_[field].startswith("-"):
            dict_[field] = "-" + attr
        else:
            dict_[field] = attr
    else:
        dict_[field] = attr

    return dict_.urlencode()

@register.filter
def singlequot(value):
    """Removes all values of arg from the given string"""
    return (value or '').replace('"', "'")
