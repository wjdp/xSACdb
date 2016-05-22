import importlib

from django import template
from django.core.urlresolvers import resolve

from xsd_frontend.nav import APP_LIST

register = template.Library()

#   0              1      2                    3                      4
# ('About xSACdb', None, 'fa fa-info-circle', 'xsd_about:AboutView', ['xsd:about:OtherView']),

def get_module_nav_list(namespace, url_name):
    try:
        nav_py = importlib.import_module("{}.nav".format(namespace))
    except ImportError:
        raise ImportError("Cannot locate nav definition module in {} namespace".format(namespace))

    module_nav = nav_py.NAV

    for section in module_nav:
        # Step through each item
        for (index, item) in enumerate(section['items']):
            # Find out if active, then apply this flag to the item list
            if (url_name == item[3] or url_name in item[4]):
                section['items'][index] = (item[0], item[1], item[2], item[3], item[4], True)
            else:
                section['items'][index] = (item[0], item[1], item[2], item[3], item[4], False)

    return module_nav


def get_page_title(module_nav, context):
    active = None
    for section in module_nav:
        for item in section['items']:
            if item[5]:
                active = item

    if active:
        if active[1] != None:
            # Specified var
            return context.get(active[1], active[0])
        else:
            return active[0]
    else:
        return 'test'

@register.inclusion_tag('nav/app.html', takes_context=True)
def app_nav(context):
    """Renders the main nav, topnav on desktop, sidenav on mobile"""
    current_url = resolve(context.request.path)
    namespace = current_url.namespaces[0]
    url_name = "{}:{}".format(namespace, current_url.url_name)

    # Set active flag on active app
    app_list = APP_LIST[:]
    for app in app_list:
        app['active'] = (app['app'] == namespace)

    context['app_list'] = APP_LIST
    context['page_title'] = get_page_title(get_module_nav_list(namespace, url_name), context)
    return context

@register.inclusion_tag('nav/module.html', takes_context=True)
def app_module_nav(context, namespace):
    """Renders the modules within the app_nav"""
    current_url = resolve(context.request.path)
    url_name = "{}:{}".format(namespace, current_url.url_name)
    module_nav = get_module_nav_list(namespace, url_name)

    context['nav'] = module_nav

    return context

@register.inclusion_tag('nav/module.html', takes_context=True)
def module_nav(context):
    """Renders module nav within apps, desktop only"""

    # Assume for our apps there only will be a single namespace
    current_url = resolve(context.request.path)
    namespace = current_url.namespaces[0]
    url_name = "{}:{}".format(namespace, current_url.url_name)

    context['namespace'] = namespace
    context['nav'] = get_module_nav_list(namespace, url_name)

    return context
