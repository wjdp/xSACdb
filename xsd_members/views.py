from xsd_members.models import MemberProfile
from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render, redirect

def view_my_profile(request):
    return view_profile(request, user=request.user)

def view_profile(request, user):
    profile = user.get_profile()

    return render(request,'xsd_members/profile.html', {'user':user, 'profile':profile, }, context_instance=RequestContext(request))
