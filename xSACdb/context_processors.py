from django.core.urlresolvers import resolve


def menu_perms(request):
    if request.user.is_authenticated():
        u=request.user
        p=u.get_profile()
        has_admin_module=u.is_superuser
        has_members_module=u.has_perm('xsd_members.add_memberprofile')
        has_sites_module=u.has_perm('xsd_sites.add_site')
        current_url = resolve(request.path_info).url_name
        return {
            'request': request,
            'user': u,
            'profile': p,
            'current_url':current_url,
            'has_admin_module':has_admin_module,
            'has_members_module':has_members_module,
            'has_sites_module':has_sites_module,
        }
    else: return {}

