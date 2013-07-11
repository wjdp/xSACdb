from xsd_members.models import MemberProfile
from django.contrib.auth.models import User

from django.views.generic.list import ListView

from django.template import RequestContext
from django.shortcuts import render, redirect

def view_my_profile(request):
    return view_profile(request, user=request.user)

def view_profile(request, user):
    profile = user.get_profile()

    return render(request,'profile.html', {'user':user, 'profile':profile, }, context_instance=RequestContext(request))

class OrderedListView(ListView):
    def get_queryset(self):
        return super(OrderedListView, self).get_queryset().order_by(self.order_by)

class MemberList(OrderedListView):
    model=User
    template_name='members_list.html'
    context_object_name='members'
    order_by='last_name'
