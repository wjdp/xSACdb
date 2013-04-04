def menu_perms(request):
    u=request.user
    has_admin_module=u.is_superuser
    has_members_module=u.has_perm('xsd_members.add_memberprofile')

    return {
        'request': request,
        'has_admin_module':has_admin_module,
        'has_members_module':has_members_module,
    }
