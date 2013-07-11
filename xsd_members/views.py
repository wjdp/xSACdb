from django.contrib.auth.models import User

from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

from xsd_members.models import MemberProfile
from xsd_members.forms import *


def view_my_profile(request):
    profile=request.user.get_profile
    editable=True
    return render(request,'members_detail.html',
        {'member_profile':profile,
        'member':request.user,
        'editable':editable,
        'myself':True},
        context_instance=RequestContext(request))

def admin(request):
    return redirect(reverse('MemberSearch'))

class OrderedListView(ListView):
    def get_queryset(self):
        return super(OrderedListView, self).get_queryset().order_by(self.order_by)

class MemberSearch(OrderedListView):
    model=User
    template_name='members_search.html'
    context_object_name='members'
    order_by='last_name'

    def get_queryset(self):
        if 'surname' in self.request.GET:
            surname=self.request.GET['surname']
            queryset=super(MemberSearch, self).get_queryset()
            queryset=queryset.filter(last_name__contains=surname)
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
    model=User
    template_name='members_list.html'
    context_object_name='members'
    order_by='last_name'

class MemberDetail(DetailView):
    model=User
    template_name='members_detail.html'
    context_object_name='member'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['member_profile']  = self.get_object().get_profile()
        context['editable']        = True
        return context

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
        return reverse('MemberDetail', kwargs={'pk':user.pk})

    def get_model(self):
        user=self.get_user()
        return user.get_profile()

