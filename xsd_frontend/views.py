from django.shortcuts import render, redirect
from django.template import RequestContext

from datetime import date

def dashboard(request):
    if request.user.is_authenticated()==False:
        return redirect('login')
    now =date.today()
    p = request.user.get_profile()
    membership_ok=True
    no_data=False

    if p.club_expiry==None or p.bsac_expiry==None or p.medical_form_expiry==None:
        no_data=True
        membership_ok=False
        club_expired=True
        bsac_expired=True
        medical_form_expired=True
    else:
        if request.user.get_profile().club_expiry <= now:
            club_expired=True
            membership_ok=False
        else: club_expired=False
        if request.user.get_profile().bsac_expiry <= now:
            bsac_expired=True        
            membership_ok=False
        else: bsac_expired=False
        if request.user.get_profile().medical_form_expiry <= now:
            medical_form_expired=True        
            membership_ok=False
        else: medical_form_expired=False

    return render(request,'xsd_frontend/dashboard.html', {
        'request':request,
        'club_expired':club_expired,
        'bsac_expired':bsac_expired,
        'medical_form_expired':medical_form_expired,
        'no_data':no_data,
        'membership_ok':membership_ok,
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
    return render(request,'xsd_frontend/login.html', {'form':form})

from django.contrib.auth import logout as auth_logout

def logout(request):
   auth_logout(request)
   return redirect('/')
