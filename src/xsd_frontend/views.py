from __future__ import unicode_literals

from allauth.account.views import LoginView, SignupView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from forms import UpdateRequestMake, ClassicSignupForm
from xSACdb.roles.mixins import RequirePreauth
from xsd_frontend.activity import XSDAction


class DashboardView(ListView):
    model = XSDAction
    paginate_by = settings.PAGINATE_BY
    context_object_name = 'feed'

    def get_queryset(self):
        return XSDAction.objects.user(self.request.user)

    def get_template_names(self):
        if self.request.user.profile.verified:
            # Is a verified club member
            return 'frontend/dashboard.html'
        else:
            # Is new
            return 'frontend/unverified_jumbo.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.user.profile.verified:
            pass
        return context


class PreauthLoginView(RequirePreauth, LoginView):
    template_name = 'preauth/login.html'


class PreauthRegisterView(RequirePreauth, SignupView):
    template_name = 'preauth/register.html'
    form_class = ClassicSignupForm


from django.contrib.auth import logout as auth_logout


def logout(request):
    # We roll our own logout view as the allauth one needs a POST
    auth_logout(request)
    return redirect('/')


def update_request(request):
    if request.POST:
        form = UpdateRequestMake(request.POST)
        form.data = form.data.copy()
        if form.is_valid():
            ur = form.save()
            ur.request_made_by = request.user
            ur.save()
            return HttpResponse(content="ok")
    response = HttpResponse(content="bad")
    response.status_code = 400
    return response


def design(request):
    return render(request, 'design.html')


def handler400(request):
    return render(request, '500.html', status=400)


def handler403(request):
    return render(request, '403.html', status=403)


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
