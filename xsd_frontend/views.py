from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext

from datetime import date

from xsd_members.forms import PersonalEditForm

from forms import UpdateRequestMake
from models import UpdateRequest

def dashboard(request):
    profile=request.user.get_profile()
    newbie=profile.new

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
    }, context_instance=RequestContext(request))

from xsd_frontend.forms import LoginForm 

def login(request):
    from django.contrib.auth import authenticate, login
    if request.method == 'POST' and request.POST:
        form=LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
            else:
                # Return a 'disabled account' error message
                pass
        else:
            form.errors.__all__=[u"Invalid username or password"]
            pass
    else:
        form=LoginForm()
    return render(request,'frontend_login.html', {'form':form}, context_instance=RequestContext(request))

from django.contrib.auth import logout as auth_logout

def logout(request):
   auth_logout(request)
   return redirect('/')

def error403(request):
    return render(request, 'error403.html')

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
