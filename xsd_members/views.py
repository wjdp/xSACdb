from django.contrib.auth.models import User

from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.forms.formsets import formset_factory

from django.db.models import Q

from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

from xsd_members.models import MemberProfile
from xsd_members.forms import *

import datetime
import StringIO
import csv

def view_my_profile(request):
    profile=request.user.get_profile
    editable=True
    return render(request,'members_detail.html',{
        'member':profile,
        'editable':editable,
        'myself':True},
        context_instance=RequestContext(request))

def admin(request):
    return redirect(reverse('MemberSearch'))

class OrderedListView(ListView):
    def get_queryset(self):
        return super(OrderedListView, self).get_queryset().order_by(self.order_by)

class MemberSearch(OrderedListView):
    model=MemberProfile
    template_name='members_search.html'
    context_object_name='members'
    order_by='user__last_name'

    def get_queryset(self):
        if 'surname' in self.request.GET:
            surname=self.request.GET['surname']
            queryset=super(MemberSearch, self).get_queryset()
            queryset=queryset.filter(user__last_name__contains=surname)
        else:
            queryset=None
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberSearch, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['search_form'] = MemberSearchForm()
        return context

class MemberList(OrderedListView):
    model=MemberProfile
    template_name='members_list.html'
    context_object_name='members'
    order_by='user__last_name'
    page_title='Club Membership Listing'

    def get_context_data(self, **kwargs):
        context = super(MemberList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class MembersExpiredFormsList(MemberList):
    page_title='Members With Expired Forms'

    def get_queryset(self):
        queryset=super(MembersExpiredFormsList, self).get_queryset()
        today=datetime.date.today()
        queryset=queryset.filter(Q(bsac_expiry__lte=today) | Q (bsac_expiry=None) | \
            Q(club_expiry__lte=today) | Q(club_expiry=today) | \
            Q(medical_form_expiry__lte=today) | Q(medical_form_expiry=None))
        return queryset

class MembersMissingFieldsList(MemberList):
    page_title='Members With Missing Personal Fields'

    blank_fields=['address','postcode','home_phone','mobile_phone','next_of_kin_name','next_of_kin_relation','next_of_kin_phone']

    def build_queryset(self):
        qObj = None
        for field in self.blank_fields:
            newQ = Q(**{field :  ''}) 
            if qObj is None:
                qObj = newQ
            else:
                qObj = qObj | newQ
        return qObj

    def get_queryset(self):
        queryset=super(MembersMissingFieldsList, self).get_queryset()
        queryset_filtered=queryset.filter(self.build_queryset())
        return queryset_filtered

class MemberDetail(DetailView):
    model=MemberProfile
    template_name='members_detail.html'
    context_object_name='member'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['editable']        = True
        return context
    def get_object(self):
        user_pk=self.kwargs['user__pk']
        user=User.objects.get(pk=user_pk)
        return user.get_profile()


class ModelFormView(FormView):
    def get_model(self):
        pass

    def get_initial(self):
        initial={}
        model=self.get_model()
        for field in self.form_class._meta.fields:
            initial[field]=getattr(model,field)
        return initial
    def form_valid(self, form):
        model=self.get_model()
        for field in form.cleaned_data:
            setattr(model, field, form.cleaned_data[field])
        model.save()
        return super(ModelFormView, self).form_valid(form)

class MyProfileEdit(ModelFormView):
    template_name='members_personal_edit.html'
    form_class=PersonalEditForm
    success_url=reverse_lazy('my-profile')

    def get_model(self):
        return self.request.user.get_profile()

class MemberEdit(ModelFormView):
    template_name='members_edit.html'
    form_class=MemberEditForm

    def get_user(self):
        pk=self.kwargs['pk']
        user=get_object_or_404(User,pk=pk)
        return user

    def get_success_url(self):
        user = self.get_user()
        return reverse('MemberDetail', kwargs={'user__pk':user.pk})

    def get_model(self):
        user=self.get_user()
        return user.get_profile()

def select_tool(request):
    return render(request,'members_bulk_select.html',{
        },
        context_instance=RequestContext(request))

class BulkAddForms(View):
    model=MemberProfile
    

    def get(self, request, *args, **kwargs):
        spreadsheet=False
        if 'set' in request.GET:
            if request.GET['set']=='all':
                members=self.get_all_objects()
            spreadsheet=True
        elif 'names' in request.GET and request.GET['names']!='':
            from bulk_select import get_bulk_members
            members=get_bulk_members(request)
            spreadsheet=True
        if spreadsheet:
            FormExpiryFormSet = formset_factory(FormExpiryForm, extra=0)
            initial=[]
            for member in members:
                initial.append({'user_id':member.user.pk})
            formset=FormExpiryFormSet(initial=initial)
            for member,form in zip(members,formset):
                form.full_name=member.user.get_full_name()

            return render(request,'members_bulk_edit_forms.html',{
                'page_title':'Bulk Select Results',
                'formset':formset,
            },
            context_instance=RequestContext(request))
        else:
            # First form
            return render(request,'members_bulk_select.html',{
            },
            context_instance=RequestContext(request))

    def get_all_objects(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        formset=FormExpiryFormSet(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                mp=MemberProfile.objects.get(user__pk=form['user_id'])
                if form['club_expiry']: mp.club_expiry=form['club_expiry']
                if form['bsac_expiry']: mp.bsac_expiry=form['bsac_expiry']
                if form['medical_form_expiry']: mp.medical_form_expiry=form['medical_form_expiry']
                mp.save()
        else:
            print "UNCLEAN!"

        return redirect(reverse('BulkAddForms'))

