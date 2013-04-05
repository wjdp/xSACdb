def menu_perms(request):
    if request.user.is_authenticated():
        u=request.user
        p=u.get_profile()
        has_admin_module=u.is_superuser
        has_members_module=u.has_perm('xsd_members.add_memberprofile')
        return {
            'request': request,
            'user': u,
            'profile': p,
            'has_admin_module':has_admin_module,
            'has_members_module':has_members_module,
        }
    else: return {}
