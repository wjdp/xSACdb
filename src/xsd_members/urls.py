

from django.conf.urls import url

from .api import *
from .views import *
from xsd_frontend.versioning import VersionHistoryView

app_name = 'xsd_members'

urlpatterns = [
    url(r'^profile/$', view_my_profile, name='my-profile'),
    url(r'^profile/edit/$', MyProfileEdit.as_view(), name='MyProfileEdit'),

    url(r'^profile/update/$', MemberProfileUpdate.as_view(), name='MemberProfileUpdate'),

    url(r'^$', admin, name='members_admin'),

    url(r'^search/$', MemberSearch.as_view(), name='MemberSearch'),

    url(r'^member/(?P<pk>\d+)/$', MemberDetail.as_view(), name='MemberDetail'),
    url(r'^member/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='MemberHistory',
        kwargs={'model': MemberProfile}),
    url(r'^member/(?P<pk>\d+)/edit/$', MemberEdit.as_view(), name='MemberEdit'),
    url(r'^member/(?P<pk>\d+)/action/(?P<action>\w+)/$', MemberAction.as_view(), name='MemberAction'),
    url(r'^member/(?P<pk>\d+)/delete/$', MemberDelete.as_view(), name='MemberDelete'),
    url(r'^member/(?P<pk>\d+)/archive/$', MemberArchive.as_view(), name='MemberArchive'),

    url(r'^list/$', MemberList.as_view(), name='MemberList'),
    url(r'^new-members/$', NewMembers.as_view(), name='NewMembers'),
    url(r'^expired-forms/$', MembersExpiredFormsList.as_view(), name='MembersExpiredFormsList'),
    url(r'^missing-fields/$', MembersMissingFieldsList.as_view(), name='MembersMissingFieldsList'),
    url(r'^archived/$', MembersArchivedList.as_view(), name='MembersArchivedList'),

    url(r'^add/forms/$', BulkAddForms.as_view(), name='BulkAddForms'),

    url(r'^api/tokeninput-data.js$', tokeninput_json, name='tokeninput-json'),

    url(r'^select/$', select_tool, name='members-select-tool'),

    url(r'^update-requests/$', MemberUpdateRequestList.as_view(), name='MemberUpdateRequestList'),
    url(r'^update-requests/save/$', MemberUpdateRequestRespond.as_view(),
        name='MemberUpdateRequestRespond'),

    url(r'^reports/overview/$', reports_overview, name='ReportsOverview'),
]
