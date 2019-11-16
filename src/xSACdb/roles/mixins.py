

from django.core.exceptions import PermissionDenied

from .functions import *


class RequireGroup:
    def is_in_group(self, user):
        return False

    def dispatch(self, request, *args, **kwargs):
        if self.is_in_group(request.user):
            return super(RequireGroup, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class RequirePermission:
    # TODO This is the old version of RequirePermission where model has permission functions.
    # TODO New version lives in xsd_auth.permissions
    def get_permission_object(self):
        """Object to check permission against"""
        return self.get_object()

    def has_permission(self, user):
        if not hasattr(self, 'permission'):
            raise ValueError('Need a permission set on this CBV')

        object_inst = self.get_permission_object()

        if hasattr(object_inst, self.permission):
            perm_func = getattr(object_inst, self.permission)
            return perm_func(user)

        else:
            raise ValueError('{0} does not have permission function {1}'.format(
                type(self.object).__name__, self.permission))

    def dispatch(self, request, *args, **kwargs):
        if self.has_permission(request.user):
            return super(RequirePermission, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class RequireVerified(RequireGroup):
    def is_in_group(self, user):
        return is_verified(user)


class RequireInstructor(RequireGroup):
    def is_in_group(self, user):
        return is_instructor(user)


class RequireTrainingOfficer(RequireGroup):
    def is_in_group(self, user):
        return is_training(user)


class RequireTripsOfficer(RequireGroup):
    def is_in_group(self, user):
        return is_trips(user)


class RequireSiteAdministrator(RequireGroup):
    def is_in_group(self, user):
        return is_sites(user)


class RequireMembersOfficer(RequireGroup):
    def is_in_group(self, user):
        return is_members(user)


class RequireDivingOfficer(RequireGroup):
    def is_in_group(self, user):
        return is_diving_officer(user)


class RequireAdministrator(RequireGroup):
    def is_in_group(self, user):
        return is_admin(user)


class RequireTrusted(RequireGroup):
    def is_in_group(self, user):
        return is_trusted(user)


from django.http import HttpResponseRedirect


class RequirePreauth:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return super(RequirePreauth, self).dispatch(request, *args, **kwargs)
