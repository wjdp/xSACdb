from django.core.exceptions import PermissionDenied

from .functions import *

class require_group:
    def __init__(self, f):
        self.f=f

    def is_allowed(self,user):
        return False

    def __call__(self,request, *args, **kwargs):
        if self.is_allowed(request.user):
            return self.f(request, *args, **kwargs)
        else:
            raise PermissionDenied

class require_verified(require_group):
    def is_allowed(self,user):
        return is_verified(user)

class require_instructor(require_group):
    def is_allowed(self,user):
        return is_instructor(user)

class require_training_officer(require_group):
    def is_allowed(self,user):
        return is_training(user)
class require_trips_officer(require_group):
    def is_allowed(self,user):
        return is_trips(user)
class require_site_administrator(require_group):
    def is_allowed(self,user):
        return is_sites(user)
class require_members_officer(require_group):
    def is_allowed(self,user):
        return is_members(user)
class require_diving_officer(require_group):
    def is_allowed(self,user):
        return is_diving_officer(user)
class require_administrator(require_group):
    def is_allowed(self,user):
        return is_admin(user)

class require_trusted(require_group):
    def is_allowed(self, user):
        return is_trusted(user)
