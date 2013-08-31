from django.shortcuts import render, redirect
from django.template import RequestContext

from datetime import date

from xsd_members.forms import PersonalEditForm

def dashboard(request):
    profile=request.user.get_profile()
    newbie=profile.new

    repost=False

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
