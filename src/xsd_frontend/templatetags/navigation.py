import importlib

from django import template
from django.core.cache.utils import make_template_fragment_key
from django.core.urlresolvers import resolve, Resolver404
from django.core.cache import cache

from xsd_frontend.nav import APP_LIST

register = template.Library()

# The structure of a navigation tuple is shown here:
#   0              1           2                    3                      4                       5
# ('About xSACdb', None,      'fa fa-info-circle', 'xsd_about:AboutView', ['xsd:about:OtherView']),
#  Item title      title var  icon                 primary url            other urls

def get_club_name(context):
    if 'l10n_club' in context:
        return context['l10n_club']['name']
    else:
        # TODO, log occurrences of this
        return 'xSACdb'


def get_module_nav_list(namespace, url_name, user):
    if not namespace:
        return None

    # Imports the navigation definition from the app/nav.py file
    try:
        nav_py = importlib.import_module("{}.nav".format(namespace))
    except ImportError:
        raise ImportError("Cannot locate nav definition module in {} namespace".format(namespace))

    module_nav = []

    for section in nav_py.NAV:
        print section['access']
        if not section['access'](user):
            # Skip adding if we don't have access
            continue
        # Step through each item
        for (index, item) in enumerate(section['items']):
            # Find out if active, then apply this flag to the item list
            if (url_name == item[3] or url_name in item[4]):
                section['items'][index] = (item[0], item[1], item[2], item[3], item[4], True)
            else:
                section['items'][index] = (item[0], item[1], item[2], item[3], item[4], False)
        # Add processed section to returned list
        module_nav.append(section)

    return module_nav


def get_page_title(module_nav, context):
    if module_nav:
        active = None
        # Iterate over sections in module nav to find current item
        # There must be a better way of doing this!
        for section in module_nav:
            for item in section['items']:
                if item[5]:
                    active = item
        # If we found the active page
        if active:
            if active[1] != None:
                # This page has asked we look at a certain variable to get the page name
                return context.get(active[1], active[0])
            else:
                # We use the page name from the nav definition
                return active[0]

    return get_club_name(context)


def get_namespace(context):
    try:
        current_url = resolve(context.request.path)
        if len(current_url.namespaces) > 0:
            return current_url.namespaces[0]
        else:
            return ""
    except Resolver404:
        return ""


def get_app_title(namespace):
    for app in APP_LIST:
        if app['app'] == namespace:
            return app['title']


def get_url_name(context):
    try:
        current_url = resolve(context.request.path)
        namespace = get_namespace(context)
        return "{}:{}".format(namespace, current_url.url_name)
    except Resolver404:
        return None


@register.simple_tag(takes_context=True)
def page_title(context):
    namespace = get_namespace(context)
    url_name = get_url_name(context)
    module_nav = get_module_nav_list(namespace, url_name, context.request.user)
    return "{} - {} - {} Database".format(get_page_title(module_nav, context), get_app_title(namespace),
                                          get_club_name(context))


@register.inclusion_tag('nav/app.html', takes_context=True)
def app_nav(context):
    """Renders the main nav, topnav on desktop, sidenav on mobile"""
    url_name = get_url_name(context)
    namespace = get_namespace(context)

    cache_id = "{}:{}".format(context['request'].user.username, context.request.path)
    cache_key = make_template_fragment_key('app_nav', [cache_id])
    context['app_nav_cache_id'] = cache_id

    # Only bother doing this work if we don't have a cached template render
    if not cache.get(cache_key):
        # Set active flag on active app
        app_list = APP_LIST[:]
        for app in app_list:
            app['active'] = (app['app'] == namespace)

        context['app_list'] = APP_LIST
        context['app'] = namespace

        if namespace:
            context['page_title'] = get_page_title(get_module_nav_list(namespace, url_name, context.request.user), context)

    return context


@register.inclusion_tag('nav/module.html', takes_context=True)
def app_module_nav(context, namespace):
    """Renders the modules within the app_nav"""
    context['nav'] = get_module_nav_list(namespace, get_url_name(context), context.request.user)
    return context


@register.inclusion_tag('nav/module.html', takes_context=True)
def module_nav(context):
    """Renders module nav within apps, desktop only"""

    # Assume for our apps there only will be a single namespace
    namespace = get_namespace(context)
    url_name = get_url_name(context)

    context['namespace'] = namespace
    context['nav'] = get_module_nav_list(namespace, url_name, context.request.user)

    return context
