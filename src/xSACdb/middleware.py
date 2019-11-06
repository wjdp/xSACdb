

from re import compile

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponseRedirect

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(object):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL + '?next=/{}'.format(path))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class NewbieProfileFormRedirectMiddleware(object):
    """
    Redirect new users to the newbie form if they're missing details from
    their profile.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        assert hasattr(request, 'user')

        CACHE_KEY = self.get_cache_key(request.user)
        path = request.path_info.lstrip('/')

        if cache.get(CACHE_KEY) is not True or (m.match(path) for m in EXEMPT_URLS):
            if request.user.is_authenticated and request.user.memberprofile.get_missing_field_list() != []:
                newbie_form_url = reverse('xsd_members:MemberProfileUpdate')
                if request.path_info != newbie_form_url:
                    return HttpResponseRedirect(newbie_form_url)
            else:
                cache.set(CACHE_KEY, True, 3600)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    @classmethod
    def get_cache_key(cls, user):
        return 'newbie_form_bypass_{}'.format(user.pk)

    @classmethod
    def invalidate_cache(cls, user):
        cache.delete(cls.get_cache_key(user))
