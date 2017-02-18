from django.core.exceptions import PermissionDenied

from functions import *

class RequireGroup(object):
    def is_allowed(self,user):
        return False
    def dispatch(self, request, *args, **kwargs):
        if self.is_allowed(request.user):
            return super(RequireGroup, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    # def get(self, request, *args, **kwargs):
    #     if self.is_allowed(request.user):
    #         return super(RequireGroup, self).get(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied

class RequireVerified(RequireGroup):
    def is_allowed(self,user):
        return is_verified(user)

class RequireInstructor(RequireGroup):
    def is_allowed(self,user):
        return is_instructor(user)

class RequireTrainingOfficer(RequireGroup):
    def is_allowed(self,user):
        return is_training(user)
class RequireTripsOfficer(RequireGroup):
    def is_allowed(self,user):
        return is_trips(user)
class RequireSiteAdministrator(RequireGroup):
    def is_allowed(self,user):
        return is_sites(user)
class RequireMembersOfficer(RequireGroup):
    def is_allowed(self,user):
        return is_members(user)
class RequireDivingOfficer(RequireGroup):
    def is_allowed(self,user):
        return is_diving_officer(user)
class RequireAdministrator(RequireGroup):
    def is_allowed(self,user):
        return is_admin(user)

class RequireTrusted(RequireGroup):
    def is_allowed(self,user):
        return is_trusted(user)

from django.http import HttpResponseRedirect

class RequirePreauth(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return super(RequirePreauth, self).dispatch(request, *args, **kwargs)
