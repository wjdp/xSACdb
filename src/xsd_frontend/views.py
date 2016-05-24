import base64

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import get_user_model

from datetime import date

from xsd_members.forms import WelcomeScreenForm

from forms import UpdateRequestMake, UserRegisterForm
from models import UpdateRequest

from xSACdb.roles.functions import is_verified, is_trusted
from xSACdb.roles.mixins import RequireTrusted


def dashboard(request):
    profile=request.user.memberprofile
    newbie=profile.new

    not_yet_verified = not is_verified(request.user)

    repost=False

    urs=UpdateRequest.objects.filter(request_made_by=request.user)

    if request.POST and newbie:
        form=WelcomeScreenForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.new=False
            profile.save()
            return redirect('/')
        else:
            repost=True
            pass
    else:
        if newbie:
            form=WelcomeScreenForm(instance=profile)
        else:
            form=None

    # TODO make a nice universal way of doing this

    if is_trusted(request.user):
        versions = get_versions_for_model(get_activity_feed_models())[:10]
        versions2 = []
        for thisVersion in versions:
            thisItem = get_changes_for_version(thisVersion, None)
            versions2.append(thisItem)
    else:
        versions = None
        versions2 = None

    return render(request,'frontend_dashboard.html', {
        'request':request,
        'profile':profile,
        'form':form,
        'newbie':newbie,
        'repost':repost,
        'versions': versions2,
        'urs':urs,
        'not_yet_verified': not_yet_verified,
    }, context_instance=RequestContext(request))

from xsd_frontend.forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    errors = None
    if request.method == 'POST' and request.POST:
        form=LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                return redirect("/")
            else:
                # Return a 'disabled account' error message
                pass
        else:
            errors = 'badauth'
            pass
    else:
        form=LoginForm()
    return render(request,'frontend_login.html', {
            'form':form,
            'errors':errors
        }, context_instance=RequestContext(request))

from django.contrib.auth import logout as auth_logout

def logout(request):
   auth_logout(request)
   return redirect('/')

def register(request):
    if request.method == 'POST' and request.POST:
        form = UserRegisterForm(request.POST)
        U = get_user_model()
        if U.objects.filter(email=request.POST['email_address']).count() != 0:
            form.errors['email_address']=['That email is already registered on this database.']
        if len(request.POST['password'])<8:
            form.errors['password']=['Password must be 8 or more characters long.']
        else:
            # Custom error checking ok
            if form.is_valid():
                #do valid stuff
                new_user = get_user_model().objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email_address'],
                    password=form.cleaned_data['password']
                )
                new_user.save()

                user = authenticate(username=form.cleaned_data['email_address'], password=form.cleaned_data['password'])

                del form.cleaned_data['password']

                dj_login(request, user)
                return redirect('/')
            else:
                pass
    else:
        form = UserRegisterForm()
    return render(request,'frontend_register.html',
        {'form': form},
        context_instance=RequestContext(request))

def update_request(request):
    if request.POST:
        form=UpdateRequestMake(request.POST)
        form.data = form.data.copy()
        if form.is_valid():
            ur=form.save()
            ur.request_made_by=request.user
            ur.save()
            return HttpResponse(content="ok")
    response=HttpResponse(content="bad")
    response.status_code=400
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
import reversion

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
