from django.core.urlresolvers import resolve, Resolver404
from django.conf import settings

from xSACdb.roles.functions import *

from xsd_frontend.forms import UpdateRequestMake
from xsd_members.forms import MyUserAccountForm

def menu_perms(request):
    if request.user.is_authenticated():
        u=request.user
        p=u.memberprofile
        try:
            current_url = resolve(request.path_info).url_name
        except Resolver404:
            current_url = ''

        update_request_form = UpdateRequestMake()
        my_user_account_form = MyUserAccountForm()

        DEBUG = settings.DEBUG
        l10n_club = settings.CLUB

        return {
            'request': request,
            'user': u,
            'profile': p,
            'current_url':current_url,

            'DEBUG': DEBUG,
            'l10n_club': l10n_club,
            'RAVEN_DSN': settings.RAVEN_CONFIG.get('dsn_public', None),

            'update_request_form':update_request_form,
            'my_user_account_form': my_user_account_form,

            'is_verified':is_verified(u),
            'is_training':is_training(u),
            'is_trips':is_trips(u),
            'is_sites':is_sites(u),
            'is_members':is_members(u),
            'is_diving_officer':is_diving_officer(u),
            'is_admin':is_admin(u),
            'is_trusted': is_trusted(u),
        }
    else: return {}

# FIXME Why doubled up?
def is_training(user):
    groups=[2,3,7]
    return is_allowed(user,groups)
def is_trips(user):
    groups=[2,3,4,7]
    return is_allowed(user,groups)
def is_sites(user):
    groups=[2,5,7]
    return is_allowed(user,groups)
def is_members(user):
    groups=[2,3,6,7]
    return is_allowed(user,groups)
def is_diving_officer(user):
    groups=[2,7]
    return is_allowed(user,groups)
def is_admin(user):
    groups=[2]
    return is_allowed(user,groups)
