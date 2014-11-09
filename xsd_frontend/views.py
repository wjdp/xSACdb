import base64

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import get_user_model

from datetime import date

from xsd_members.forms import PersonalEditForm

from forms import UpdateRequestMake, UserRegisterForm
from models import UpdateRequest

from xSACdb.roles.functions import is_verified


def dashboard(request):
    profile=request.user.memberprofile
    newbie=profile.new

    not_yet_verified = not is_verified(request.user)

    repost=False

    urs=UpdateRequest.objects.filter(request_made_by=request.user)

    if request.POST and newbie:
        form=PersonalEditForm(request.POST, instance=profile)
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
            form=PersonalEditForm(instance=profile)
        else:
            form=None

    return render(request,'frontend_dashboard.html', {
        'request':request,
        'profile':profile,
        'form':form,
        'newbie':newbie,
        'repost':repost,
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
    return render(request,'frontend_login.html', {'form':form, 'errors':errors}, context_instance=RequestContext(request))

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
                new_user = get_user_model()
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.email = form.cleaned_data['email_address']
                new_user.set_password(form.cleaned_data['password'])
                # new_user.username = base64.b64encode(new_user.email)
                new_user.save()
                user = authenticate(email=new_user.email, password=form.cleaned_data['password'])
                del form.cleaned_data['password']
                dj_login(request, user)
                return redirect('/')
            else:
                pass
    else:
        form = UserRegisterForm()
    return render(request,'frontend_register.html', {'form': form})

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
