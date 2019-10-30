

from django import template

register = template.Library()

@register.filter()
def xsd_field_type(field):
    return field.field.__class__.__name__.lower().replace('field', '')
