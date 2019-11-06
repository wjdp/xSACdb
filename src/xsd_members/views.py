

import datetime

import reversion
from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.edit import FormView, DeleteView

from xSACdb.roles.decorators import require_members_officer
from xSACdb.roles.mixins import RequireMembersOfficer
from xSACdb.views import OrderedListView, ActionView
from xsd_frontend.activity import DoAction
from xsd_members.forms import *


def view_my_profile(request):
    profile = request.user.memberprofile
    editable = True
    return render(request, 'xsd_members/member/detail.html', {
        'member': profile,
        'editable': editable,
        'myself': True}
                  )


def admin(request):
    return redirect(reverse('xsd_members:MemberSearch'))


class MemberProfileUpdate(FormView):
    template_name = "xsd_members/member/update.html"
    success_url = "/"
    form_class = MemberProfileUpdateForm

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        return form_class(instance=self.request.user.profile, **self.get_form_kwargs())

    def form_valid(self, form):
        # Form still holds ref to MemberProfile so handles saving all by itself
        with DoAction() as action, reversion.create_revision():
            if self.request.user.profile.archived:
                # User logged back in and re-added details. Reinstate
                form.save()
                # Done bare as we are building our own action here
                self.request.user.profile.reinstate(bare=True)
                action.set(actor=self.request.user, verb='reinstated',
                           target=self.request.user.profile, style='mp-dynamic-reinstate')
            else:
                form.save()
                action.set(actor=self.request.user, verb='updated',
                           target=self.request.user.profile, style='mp-dynamic-update')

        messages.add_message(self.request, messages.SUCCESS, settings.CLUB['memberprofile_update_success'])

        return super(MemberProfileUpdate, self).form_valid(form)


class MemberSearch(RequireMembersOfficer, OrderedListView):
    model = MemberProfile
    template_name = 'xsd_members/member/search.html'
    context_object_name = 'members'
    order_by = 'last_name'

    def get_queryset(self):
        if 'q' in self.request.GET:
            name = self.request.GET['q']
            queryset = super(MemberSearch, self).get_queryset()
            queryset = queryset.filter(
                Q(last_name__icontains=name) |
                Q(first_name__icontains=name)
            )
            queryset = queryset.prefetch_related('user', 'top_qual_cached', 'club_membership_type')
        else:
            queryset = None

        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberSearch, self).get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['q'] = self.request.GET['q']
        return context


class MemberList(RequireMembersOfficer, OrderedListView):
    model = MemberProfile
    template_name = 'members_list.html'
    context_object_name = 'members'
    order_by = 'last_name'
    page_title = 'Club Membership Listing'
    page_description = 'Our entire membership (that has registered for the database)'

    def get_context_data(self, **kwargs):
        context = super(MemberList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        return context

    def get_queryset(self, *args, **kwargs):
        show_archived = kwargs.pop('show_archived', False)
        q = super(MemberList, self).get_queryset(*args, **kwargs)
        if not show_archived:
            # Hide archived members
            q = q.filter(archived=False)
        # Prefetch some stuff to cut down number of queries
        q_prefetch = q.prefetch_related('user', 'top_qual_cached', 'club_membership_type')
        return q_prefetch


class NewMembers(MemberList):
    page_title = 'New Members'
    page_description = 'After members signup they require approval from a members officer to use the database. To ' \
                       'approve use the <div class="fake-button"><i class="fa fa-check"></i> Approve</div> button on ' \
                       'their profile page. Before this you\'ll probably want to add details to their profile.'

    def get_queryset(self):
        queryset = super(NewMembers, self).get_queryset()
        queryset = queryset.filter(new_notify=True)
        return queryset


class MembersExpiredFormsList(MemberList):
    page_title = 'Members With Expired Forms'
    page_description = '''<p><i class="icon-bsac-small expired"></i>is expired
        BSAC membership, <i class="fa fa-home expired"></i>is expired club
        membership and <i class="fa fa-medkit expired"></i>is an expired
        medical form.</p>
        <p>The easiest way of bulk adding forms is the Bulk Jobs <i class="fa fa-arrow-right"></i> Add Forms
        Tool.</p>'''

    def get_queryset(self):
        queryset = super(MembersExpiredFormsList, self).get_queryset()
        today = datetime.date.today()
        queryset = queryset.filter(Q(bsac_expiry__lte=today) | Q(bsac_expiry=None) | \
                                   Q(club_expiry__lte=today) | Q(club_expiry=today) | \
                                   Q(medical_form_expiry__lte=today) | Q(medical_form_expiry=None))
        return queryset


class MembersMissingFieldsList(MemberList):
    page_title = 'Members With Missing Personal Fields'
    page_description = '''<p>The only reason a member will be on this list is
        that they failed to fill out the form shown to them when they signed up
        to the database. This form will be shown to them when they log in
        again, they will not be able to use other parts of the database until
        this form is completed.</p>'''

    blank_fields = MemberProfile.PERSONAL_FIELDS

    def build_queryset(self):
        qObj = None
        for field in self.blank_fields:
            newQ = Q(**{field: ''})
            if qObj is None:
                qObj = newQ
            else:
                qObj = qObj | newQ
        return qObj

    def get_queryset(self):
        queryset = super(MembersMissingFieldsList, self).get_queryset()
        queryset_filtered = queryset.filter(self.build_queryset())
        return queryset_filtered


class MembersArchivedList(MemberList):
    page_title = 'Archived Members'
    page_description = '''<p>Members are archived either manually by a Members Officer pressing the archive button, or
        automatically after a predefined period of inactivity. Personal data is expunged.</p>'''

    def get_queryset(self):
        queryset = super(MembersArchivedList, self).get_queryset(show_archived=True)
        return queryset.filter(archived=True)


class MemberDetail(RequireMembersOfficer, DetailView):
    model = MemberProfile
    template_name = 'xsd_members/member/detail.html'
    context_object_name = 'member'
    accounts_settings_open = False
    member_useraccount_form = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemberDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.get_object().full_name
        # Add in a QuerySet of all the books
        context['editable'] = True
        if self.request.POST:
            context['account_settings_open'] = True
        else:
            context['account_settings_open'] = False
        if self.member_useraccount_form:
            context['member_useraccount_form'] = self.member_useraccount_form
        else:
            context['member_useraccount_form'] = self.generate_account_form(
                self.get_object().user)

        return context

    def generate_account_form(self, user):
        if self.request.POST:
            return UserAccountForm(self.request.POST)
        else:
            return UserAccountForm(
                initial={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                }
            )

    def process_account_form(self, user):
        form = UserAccountForm(self.request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            if form.cleaned_data['new_password'] != "":
                user.set_password(form.cleaned_data['new_password'])
                del form.cleaned_data['new_password']
            user.save()
            return True
        return False

    def post(self, request, *args, **kwargs):
        self.get_object()
        if self.process_account_form(self.get_object().user):
            return redirect('.')
        return super(MemberDetail, self).get(request, *args, **kwargs)


class MemberAction(RequireMembersOfficer, ActionView):
    model = MemberProfile

    def approve(self, request):
        mp = self.get_object()
        mp.approve(request.user)
        messages.add_message(request, messages.SUCCESS,
                             settings.CLUB['memberprofile_approve_success'].format(mp.get_full_name(),
                                                                                   mp.heshe().lower()))

    def reinstate(self, request):
        mp = self.get_object()
        mp.reinstate(request.user)
        messages.add_message(self.request, messages.SUCCESS,
                             settings.CLUB['memberprofile_reinstate_success'].format(mp.get_full_name()))


class ModelFormView(FormView):
    def get_object(self):
        pass

    def get_initial(self):
        initial = {}
        model = self.get_object()
        for field in self.form_class._meta.fields:
            initial[field] = getattr(model, field)
        return initial

    def form_valid(self, form):
        model = self.get_object()
        for field in form.cleaned_data:
            setattr(model, field, form.cleaned_data[field])
        with DoAction() as action, reversion.create_revision():
            action.set(actor=self.request.user, verb='updated', target=model, style='mp-update')
            model.save()
        return super(ModelFormView, self).form_valid(form)


class MyProfileEdit(ModelFormView):
    template_name = 'xsd_members/member/edit.html'
    form_class = PersonalEditForm
    success_url = reverse_lazy('xsd_members:my-profile')

    def get_object(self):
        return self.request.user.memberprofile

    def get_context_data(self, **kwargs):
        context = super(MyProfileEdit, self).get_context_data(**kwargs)
        context['member'] = self.get_object()
        return context


class MemberEdit(RequireMembersOfficer, ModelFormView):
    template_name = 'xsd_members/member/edit.html'
    form_class = MemberEditForm

    def get_object(self):
        pk = self.kwargs['pk']
        mp = get_object_or_404(MemberProfile, pk=pk)
        return mp

    def get_success_url(self):
        mp = self.get_object()
        return reverse('xsd_members:MemberDetail', kwargs={'pk': mp.pk})

    def get_context_data(self, **kwargs):
        context = super(MemberEdit, self).get_context_data(**kwargs)
        context['member'] = self.get_object()
        context['page_title'] = 'Edit Profile'
        return context


class MemberDelete(RequireMembersOfficer, DeleteView):
    model = MemberProfile
    template_name = 'members_delete.html'
    success_url = reverse_lazy('xsd_members:MemberList')
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(MemberDelete, self).get_context_data()
        context['page_title'] = 'Delete Profile'
        return context


# This view very much modeled after DeletionMixin
class MemberArchive(RequireMembersOfficer, SingleObjectTemplateResponseMixin, BaseDetailView):
    model = MemberProfile
    template_name = 'members_archive.html'
    success_url = reverse_lazy('xsd_members:MemberList')
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(MemberArchive, self).get_context_data()
        context['page_title'] = 'Archive Profile'
        return context

    def archive(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.object.get_absolute_url()
        self.object.archive(request.user)
        messages.add_message(self.request, messages.SUCCESS,
                             settings.CLUB['memberprofile_archive_success'].format(self.object.get_full_name()))
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.archive(request, *args, **kwargs)


@require_members_officer
def select_tool(request):
    return render(request, 'members_bulk_select.html')


class BulkAddForms(RequireMembersOfficer, View):
    model = MemberProfile

    def get(self, request, *args, **kwargs):
        spreadsheet = False
        if 'set' in request.GET:
            if request.GET['set'] == 'all':
                members = self.get_all_objects().order_by('last_name')
            spreadsheet = True
        elif 'names' in request.GET and request.GET['names'] != '':
            from .bulk_select import get_bulk_members
            members = get_bulk_members(request, method="GET")
            spreadsheet = True
        if spreadsheet:
            FormExpiryFormSet = formset_factory(FormExpiryForm, extra=0)
            initial = []
            for member in members:
                initial.append({'member_id': member.pk})
            formset = FormExpiryFormSet(initial=initial)
            for member, form in zip(members, formset):
                form.full_name = member.get_full_name()

            return render(request, 'members_bulk_edit_forms.html', {
                'page_title': 'Bulk Select Results',
                'formset': formset,
            })
        else:
            # First form
            return render(request, 'members_bulk_select.html', {
                'content': '<h3 class="no-top"><i class="fa fa-plus"></i> Bulk Add Forms</h3><p>This tool sets the expiry dates for club, BSAC and medical forms on multiple records. The record set can either be subset of members or the entire membership.</p>'
            })

    def get_all_objects(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        formset = FormExpiryFormSet(request.POST)
        if formset.is_valid():
            with DoAction() as action, reversion.create_revision():
                reversion.set_comment('Bulk adding forms')
                reversion.set_user(request.user)
                mps = []
                for form in formset.cleaned_data:
                    mp = MemberProfile.objects.get(pk=form['member_id'])
                    if form['club_expiry']: mp.club_expiry = form['club_expiry']
                    if form['bsac_expiry']: mp.bsac_expiry = form['bsac_expiry']
                    if form['medical_form_expiry']: mp.medical_form_expiry = form['medical_form_expiry']
                    mp.save()
                    mps.append(mp)
                action.set(actor=request.user, verb="updated forms on", target=mps, style='mp-update-forms')
        else:
            return render(request, 'members_bulk_edit_forms_error.html', {})

        return redirect(reverse('xsd_members:BulkAddForms'))


from xsd_frontend.base import BaseUpdateRequestList, BaseUpdateRequestRespond


class MemberUpdateRequestList(RequireMembersOfficer, BaseUpdateRequestList):
    template_name = "members_update_request.html"
    area = 'mem'
    form_action = reverse_lazy('xsd_members:MemberUpdateRequestRespond')
    custom_include = 'members_update_request_custom.html'

    def get_queryset(self, *args, **kwargs):
        # Prefetch some stuff to cut down number of queries
        q = super(MemberUpdateRequestList, self).get_queryset(*args, **kwargs)
        q_prefetch = q.prefetch_related('request_made_by')
        return q_prefetch


class MemberUpdateRequestRespond(RequireMembersOfficer, BaseUpdateRequestRespond):
    success_url = reverse_lazy('xsd_members:MemberUpdateRequestList')


@require_members_officer
def reports_overview(request):
    data = {}
    data['member_current_count'] = MemberProfile.objects.all().filter(archived=False).count()
    data['member_archived_count'] = MemberProfile.objects.all().filter(archived=True).count()
    today = datetime.date.today()
    data['member_count_forms'] = MemberProfile.objects.filter(Q(bsac_expiry__lte=today) | Q(bsac_expiry=None) | \
                                                              Q(club_expiry__lte=today) | Q(club_expiry=today) | \
                                                              Q(medical_form_expiry__lte=today) | Q(
        medical_form_expiry=None)).count()
    return render(request, 'members_reports_overview.html', {'data': data, })
