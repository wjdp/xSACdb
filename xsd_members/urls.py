from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from api import *

members_api = Api(api_name='members')
members_api.register(MemberResource())
members_api.register(UserResource())
members_api.register(TokenInputResource())

from views import *

urlpatterns = patterns('',
	    url(r'^profile/$', 'xsd_members.views.view_my_profile', name='my-profile'),
	    url(r'^profile/edit/$', MyProfileEdit.as_view(), name='MyProfileEdit'),
	    url(r'^$', 'xsd_members.views.admin', name='members_admin'),
	    url(r'^search/$', MemberSearch.as_view(), name='MemberSearch'),
	    url(r'^member/(?P<user__pk>\d+)/$', MemberDetail.as_view(), name='MemberDetail'),
	    url(r'^member/(?P<pk>\d+)/edit/$', MemberEdit.as_view(), name='MemberEdit'),
	    url(r'^list/$', MemberList.as_view(), name='MemberList'),
	    url(r'^expired-forms/$', MembersExpiredFormsList.as_view(), name='MembersExpiredFormsList'),
	    url(r'^missing-fields/$', MembersMissingFieldsList.as_view(), name='MembersMissingFieldsList'),
	    url(r'^add/forms/$', BulkAddForms.as_view(), name='BulkAddForms'),
	    url(r'^api/',include(members_api.urls)),
	    url(r'^api/tokeninput-data/$', 'xsd_members.api.tokeninput_json', name='tokeninput-json'),
	    url(r'^select/$', 'xsd_members.views.select_tool', name='members-select-tool'),
)
