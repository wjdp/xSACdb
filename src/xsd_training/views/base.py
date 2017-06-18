from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied

from xsd_training.forms import *


class TraineeViewMixin(object):
    def get_trainee(self):
        return MemberProfile.objects.get(pk=self.kwargs['t_pk'])

    def is_allowed(self, user):
        return self.get_trainee() == user.profile or is_instructor(user)

    def dispatch(self, request, *args, **kwargs):
        if self.is_allowed(request.user):
            return super(TraineeViewMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class TraineeFormMixin(TraineeViewMixin, object):
    def get_context_data(self, **kwargs):
        context = super(TraineeFormMixin, self).get_context_data(**kwargs)
        context['trainee'] = self.get_trainee()
        return context
