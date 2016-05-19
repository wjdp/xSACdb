import importlib

from django import template
from django.core.urlresolvers import resolve

register = template.Library()

@register.inclusion_tag('nav/module.html', takes_context=True)
def module_nav(context):
    current_url = resolve(context.request.path)
    # Assume for our apps there only will be a single namespace
    namespace = current_url.namespaces[0]
    context['namespace'] = namespace
    context['url_name'] = "{}:{}".format(
        namespace, current_url.url_name
    )

    try:
        nav = importlib.import_module("{}.nav".format(namespace))
    except ImportError:
        raise ImportError("Cannot locate nav definition module in {} namespace".format(namespace))

    context['nav'] = nav.NAV

    return context
