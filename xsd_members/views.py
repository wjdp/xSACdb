from xsd_members.models import MemberProfile
from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render, redirect

def view_profile(request, username=None):
    if username==None:
        u=request.user
    else:
        u=User.objects.get(username=username)
    
    profile = u.get_profile()

    return render(request,'xsd_members/profile.html', {'user':u, 'profile':profile, }, context_instance=RequestContext(request))
