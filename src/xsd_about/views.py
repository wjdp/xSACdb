

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.views.generic.base import TemplateView

from xSACdb.environment import get_time, PRE_FILE, POST_FILE, DEPLOY_FILE
from xSACdb.roles.mixins import RequireVerified, is_admin
from xSACdb.version import *


class AboutView(RequireVerified, TemplateView):
    template_name = 'about_about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['version'] = VERSION
        if is_admin(self.request.user):
            context['build_time_pre'] = get_time(PRE_FILE)
            context['build_time_post'] = get_time(POST_FILE)
            context['build_time_deploy'] = get_time(DEPLOY_FILE)
        return context


class DatabaseOfficersView(RequireVerified, TemplateView):
    template_name = 'about_database_officers.html'

    def get_users_in_role(self, role):
        return Group.objects.get(pk=role).user_set.all()

    def get_instructors(self):
        U = get_user_model()
        return U.objects.filter(memberprofile__is_instructor_cached=True)

    def get_context_data(self, **kwargs):
        context = super(DatabaseOfficersView, self).get_context_data(**kwargs)
        context['admins'] = self.get_users_in_role(2)
        context['dos'] = self.get_users_in_role(7)
        context['mos'] = self.get_users_in_role(6)
        context['tos'] = self.get_users_in_role(3)
        context['instructors'] = self.get_instructors()
        context['tas'] = self.get_users_in_role(4)
        context['sas'] = self.get_users_in_role(5)
        return context
