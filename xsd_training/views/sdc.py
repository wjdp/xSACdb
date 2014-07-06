from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse_lazy

from xSACdb.view_helpers import OrderedListView
from xSACdb.roles.decorators import require_training_officer
from xSACdb.roles.mixins import RequireTrainingOfficer

from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table

from xsd_members.bulk_select import get_bulk_members

import re


class SDCList(OrderedListView):
    model=SDC
    template_name='sdc_list.html'
    context_object_name='sdcs'
    order_by='title'

    def get_queryset(self):
        return super(SDCList, self).get_queryset().prefetch_related('interested_members')

    def get_categories(self, top_qual):
        cats=SDC_TYPE_CHOICES
        categories=[]
        for cat in cats:
            c=SDCCategoryList(cat[0],cat[1])
            c.sdcs=SDC.objects.filter(category=cat[0]).order_by('min_qualification')
            categories.append(c)
        return categories

    def get_context_data(self, **kwargs):
        self.categories=self.get_categories(self.request.user.get_profile().top_qual())
        context = super(SDCList, self).get_context_data(**kwargs)
        context['categories']=self.categories
        return context


def sdc_register_interest(request):
    if request.POST:
        user=request.user
        sdc_id=request.POST['sdc_id']
        sdc=SDC.objects.get(pk=sdc_id)
        if request.POST['action']=="add":
            sdc.interested_members.add(user) 
        elif request.POST['action']=="remove":
            sdc.interested_members.remove(user) 
        sdc.save()
        return HttpResponse(content="True")
    else:
        return HttpResponse(content="False")

class PerformedSDCCreate(RequireTrainingOfficer, CreateView):
    model=PerformedSDC
    fields=['sdc','datetime','notes']
    template_name='performedsdc_create.html'
    form_class=PerformedSDCCreateForm

class PerformedSDCList(ListView):
    model=PerformedSDC
    template_name='performedsdc_list.html'
    context_object_name='psdc'

    def get_queryset(self):
        queryset=super(PerformedSDCList, self).get_queryset()
        queryset=queryset.filter(completed=False)
        return queryset

class PerformedSDCDetail(DetailView):
    model=PerformedSDC
    template_name='performedsdc_detail.html'
    context_object_name='psdc'

class PerformedSDCUpdate(RequireTrainingOfficer,UpdateView):
    model=PerformedSDC
    template_name='performedsdc_update.html'
    context_object_name='psdc'
    form_class=PerformedSDCUpdateForm

    def get_context_data(self, **kwargs):
        context = super(PerformedSDCUpdate, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        context['trainees']=context[self.context_object_name].trainees.all()
        return context

    def add_trainees(self, request):
        members=get_bulk_members(request)
        for member in members:
            if member.user not in self.object.trainees.all():
                self.object.trainees.add(member.user)
        self.object.save()

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        if 'names' in request.GET:
            self.add_trainees(request)
        trainee_table.remove_trainee(request, self.object)
        return super(PerformedSDCUpdate, self).get(request, *args, **kwargs)

class PerformedSDCComplete(RequireTrainingOfficer,DetailView):
    model=PerformedSDC
    template_name='performedsdc_complete.html'
    context_object_name='psdc'

    def get_users(self,request):
        users=[]
        for item in request.POST:
            if re.match('user',item):
                user_pk=item[5:]
                u=User.objects.get(pk=user_pk)
                users.append(u)
        return users

    def post(self, request, *args, **kwargs):
        users=self.get_users(request)
        psdc=self.get_object()
        sdc=psdc.sdc
        for user in users:
            p=user.get_profile()
            p.sdcs.add(sdc)
            p.save()
        for user in psdc.trainees.all():
            if user not in users:
                psdc.trainees.remove(user)
        psdc.completed=True
        psdc.save()
        return redirect(reverse('PerformedSDCList'))
        

class PerformedSDCDelete(RequireTrainingOfficer,DeleteView):
    model=PerformedSDC
    template_name='performedsdc_delete.html'
    context_object_name='psdc'
    success_url = reverse_lazy('PerformedSDCList')
