from django.shortcuts import render, redirect
from django.template import RequestContext

from datetime import date

def dashboard(request):
    if request.user.is_authenticated()==False:
        return redirect('login')
    profile=request.user.get_profile()

    return render(request,'frontend_dashboard.html', {
        'request':request,
        'profile':profile,
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
