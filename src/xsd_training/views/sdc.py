from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import RequestContext

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.urlresolvers import reverse_lazy

from xSACdb.views import OrderedListView, ActionView
from xSACdb.roles.decorators import require_training_officer, require_verified
from xSACdb.roles.mixins import RequireTrainingOfficer, RequireVerified

from xsd_members.models import MemberProfile
from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table

from xsd_members.bulk_select import get_bulk_members

import re


class SDCList(RequireVerified, OrderedListView):
    model = SDC
    template_name = 'sdc_list.html'
    context_object_name = 'sdcs'
    order_by = 'title'

    def get_queryset(self):
        return super(SDCList, self).get_queryset().prefetch_related('interested_members')

    def get_categories(self, top_qual):
        cats = SDC_TYPE_CHOICES
        categories = []
        for cat in cats:
            c = SDCCategoryList(cat[0], cat[1])
            c.sdcs = SDC.objects.filter(category=cat[0]).order_by('min_qualification')
            categories.append(c)
        return categories

    def get_context_data(self, **kwargs):
        self.categories = self.get_categories(self.request.user.memberprofile.top_qual())
        context = super(SDCList, self).get_context_data(**kwargs)
        context['categories'] = self.categories
        return context


@require_verified
def sdc_register_interest(request):
    if request.POST:
        member = request.user.memberprofile
        sdc_id = request.POST['sdc_id']
        sdc = SDC.objects.get(pk=sdc_id)
        if request.POST['action'] == "add":
            sdc.interested_members.add(member)
        elif request.POST['action'] == "remove":
            sdc.interested_members.remove(member)
        sdc.save()
        return HttpResponse(content="True")
    else:
        return HttpResponse(content="False")


class PerformedSDCCreate(RequireTrainingOfficer, CreateView):
    model = PerformedSDC
    template_name = 'performedsdc_create.html'
    form_class = PerformedSDCCreateForm


class PerformedSDCList(RequireVerified, ListView):
    model = PerformedSDC
    template_name = 'performedsdc_list.html'
    context_object_name = 'psdc'

    def get_queryset(self):
        queryset = super(PerformedSDCList, self).get_queryset()
        queryset = queryset.filter(completed=False).order_by('datetime')
        return queryset


class PerformedSDCDetail(RequireVerified, DetailView):
    model = PerformedSDC
    template_name = 'performedsdc_detail.html'
    context_object_name = 'psdc'


class PerformedSDCUpdate(RequireTrainingOfficer, UpdateView):
    model = PerformedSDC
    template_name = 'performedsdc_update.html'
    context_object_name = 'psdc'
    form_class = PerformedSDCUpdateForm

    def get_context_data(self, **kwargs):
        context = super(PerformedSDCUpdate, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        context['trainees'] = context[self.context_object_name].trainees.all()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        trainee_table.remove_trainee(request, self.object)
        return super(PerformedSDCUpdate, self).get(request, *args, **kwargs)


class PerformedSDCAction(RequireTrainingOfficer, ActionView):
    model = PerformedSDC

    def add(self, request):
        members = get_bulk_members(request)
        self.get_object().add_trainees(members, request.user)
        return reverse('xsd_training:PerformedSDCUpdate', kwargs={'pk': self.get_object().pk})

    def remove(self, request):
        members = get_bulk_members(request)
        self.get_object().remove_trainees(members, request.user)
        return reverse('xsd_training:PerformedSDCUpdate', kwargs={'pk': self.get_object().pk})


class PerformedSDCComplete(RequireTrainingOfficer, DetailView):
    model = PerformedSDC
    template_name = 'performedsdc_complete.html'
    context_object_name = 'psdc'

    def get_trainees(self, request):
        trainees = []
        for item in request.POST:
            if re.match('trainee', item):
                trainee_pk = item[8:]
                trainees.append(MemberProfile.objects.get(pk=trainee_pk))
        return trainees

    def post(self, request, *args, **kwargs):
        trainees = self.get_trainees(request)
        psdc = self.get_object()
        sdc = psdc.sdc
        for trainee in trainees:
            trainee.sdcs.add(sdc)
            trainee.save()
        for trainee in psdc.trainees.all():
            if trainee not in trainees:
                psdc.trainees.remove(trainee)
        psdc.completed = True
        psdc.save()
        return redirect(reverse('xsd_training:PerformedSDCList'))


class PerformedSDCDelete(RequireTrainingOfficer, DeleteView):
    model = PerformedSDC
    template_name = 'performedsdc_delete.html'
    context_object_name = 'psdc'
    success_url = reverse_lazy('xsd_training:PerformedSDCList')


@require_training_officer
def SDCAward(request):
    sdc_form = None
    selected_members = None
    template_name = 'sdc_award.html'

    if 'names' in request.GET and request.GET['names'] != '':
        selected_members = get_bulk_members(request)
        sdc_form = SDCSelectForm(initial={'selected_members': selected_members})

    if request.POST:
        sdc_form = SDCSelectForm(request.POST)
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
