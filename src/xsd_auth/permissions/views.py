from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied


class RequireAllowed(object):
    def dispatch(self, request, *args, **kwargs):
        if self.is_allowed(request.user):
            return super(RequireAllowed, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class RequireObjectPermission(object):
    def get_permission_object(self):
        """Object to check permission against"""
        return self.get_object()

    def has_permission(self, user):
        # Check the view using this mixin has permissions
        if not hasattr(self, 'permission'):
            raise ValueError('Need a permission set on this CBV')

        object_inst = self.get_permission_object()

        if not hasattr(object_inst, 'permissions'):
            raise Exception('No permissions object on {model}'.format(model=object_inst.__class__.__name__))

        if hasattr(object_inst.permissions, self.permission):
            perm_func = getattr(object_inst.permissions, self.permission)
            return perm_func(user)
        else:
            raise ValueError('{0} does not have permission function {1}'.format(
                object_inst.permissions.__class__.__name__, self.permission))

    def dispatch(self, request, *args, **kwargs):
        if self.has_permission(request.user):
            return super(RequireObjectPermission, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
