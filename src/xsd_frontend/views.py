from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from forms import UpdateRequestMake, UserRegisterForm
from xSACdb.roles.mixins import RequireTrusted, RequirePreauth


class DashboardView(TemplateView):
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


from xsd_frontend.forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login


class PreauthLoginView(RequirePreauth, FormView):
    template_name = 'preauth/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(PreauthLoginView, self).form_valid(form)


class PreauthRegisterView(RequirePreauth, FormView):
    template_name = 'preauth/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        new_user = get_user_model().objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        new_user.save()
        new_user_actual = authenticate(username=form.cleaned_data['email'],
                                       password=form.cleaned_data['password'])
        login(self.request, new_user_actual)

        return super(PreauthRegisterView, self).form_valid(None)


from django.contrib.auth import logout as auth_logout


def logout(request):
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


from django.views.generic import ListView
from xSACdb.versioning import get_versions_for_model, get_changes_for_version, get_activity_feed_models


class ActivityTable(RequireTrusted, ListView):
    template_name = "activity_table.html"
    paginate_by = 25

    def get_queryset(self):
        versions = get_versions_for_model(get_activity_feed_models())
        return versions

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ActivityTable, self).get_context_data(**kwargs)

        items = []

        for thisVersion in context['object_list']:
            thisItem = get_changes_for_version(thisVersion, None)
            items.append(thisItem)

        context['object_list'] = items

        return context
