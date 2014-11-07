from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse_lazy

from xSACdb.view_helpers import OrderedListView
from xSACdb.roles.decorators import require_training_officer, require_verified
from xSACdb.roles.mixins import RequireTrainingOfficer, RequireVerified

from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table

from xsd_members.bulk_select import get_bulk_members

import re


class SDCList(RequireVerified, OrderedListView):
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
        self.categories=self.get_categories(self.request.user.memberprofile.top_qual())
        context = super(SDCList, self).get_context_data(**kwargs)
        context['categories']=self.categories
        return context

@require_verified
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

class PerformedSDCList(RequireVerified, ListView):
    model=PerformedSDC
    template_name='performedsdc_list.html'
    context_object_name='psdc'

    def get_queryset(self):
        queryset=super(PerformedSDCList, self).get_queryset()
        queryset=queryset.filter(completed=False)
        return queryset

class PerformedSDCDetail(RequireVerified, DetailView):
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
            p=user.memberprofile
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

@require_training_officer
def SDCAward(request):
    sdc_form=None
    selected_members=None
    template_name = 'sdc_award.html'

    if 'names' in request.GET and request.GET['names']!='':
        selected_members=get_bulk_members(request)
        sdc_form=SDCSelectForm(initial={'selected_members':selected_members})

    if request.POST:
        sdc_form=SDCSelectForm(request.POST)
        if sdc_form.is_valid():
            for member in sdc_form.cleaned_data['selected_members']:
                member.sdcs.add(sdc_form.cleaned_data['sdc'])
                member.save()
            return render(request, template_name, {
                'completed': True,
                'selected_members': sdc_form.cleaned_data['selected_members'],
                'sdc': sdc_form.cleaned_data['sdc'],
            }, context_instance=RequestContext(request))

    return render(request, template_name, {
        'sdc_form': sdc_form,
        'selected_members': selected_members,
        'completed': False
    }, context_instance=RequestContext(request))