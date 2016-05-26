from __future__ import unicode_literals
import json

from xSACdb.test_helpers import BaseTest, ViewTestMixin, AsGroupMixin
from xSACdb.roles.groups import GROUP_MEMBERS
from xsd_members.views import *


class ProfileViewTest(ViewTestMixin, BaseTest):
    url_name = 'xsd_members:my-profile'
    template_name = 'members_detail.html'
    allowed_unverified = True


class ProfileEditViewTest(ViewTestMixin, BaseTest):
    url_name = 'xsd_members:MyProfileEdit'
    view = MyProfileEdit
    allowed_unverified = True


class MemberSearchTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberSearch'
    view = MemberSearch

    def test_search(self):
        # Do search for user, ensure user's name is in response
        u = self.create_a_user()
        c = self.get_client()
        r = c.get("{}?surname={}".format(
            self.get_url(),
            u.last_name,
        ))
        self.assertEqual(200, r.status_code)
        self.assertContains(r, u.first_name)#, html=True)
        self.assertContains(r, u.last_name)#, html=True)


class MemberDetailTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberDetail'
    view = MemberDetail

    def setUp_test(self):
        self.test_user = self.create_a_user()
        self.url_kwargs = {'pk': self.test_user.memberprofile.pk}

    def test_member_detail(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#

class MemberEditTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberEdit'
    view = MemberEdit

    def setUp_test(self):
        self.test_user = self.create_a_user()
        self.url_kwargs = {'pk': self.test_user.memberprofile.pk}

    def test_member_detail(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

        # TODO perform an edit


class MemberDeleteTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberDelete'
    view = MemberDelete

    def setUp_test(self):
        self.test_user = self.create_a_user()
        self.url_kwargs = {'pk': self.test_user.memberprofile.pk}

    def test_member_delete(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

        # TODO delete user


class MemberListTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberList'
    view = MemberList

    def setUp_test(self):
        self.test_user = self.create_a_user()

    def test_member_in_list(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)


class NewMembersTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:NewMembers'
    view = NewMembers

    def setUp_test(self):
        self.test_user = self.create_a_user()

    def test_member_in_list(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_member_not_in_list(self):
        self.test_user.memberprofile.new_notify = False
        self.test_user.memberprofile.save()
        r = self.get_response()
        self.assertNotContains(r, self.test_user.first_name)#, html=True)
        self.assertNotContains(r, self.test_user.last_name)#, html=True)


class MembersExpiredFormsListTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MembersExpiredFormsList'
    view = MembersExpiredFormsList

    def setUp_test(self):
        self.test_user = self.create_a_user()

    def test_member_in_list(self):
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_member_not_in_list(self):
        self.test_user.memberprofile.bsac_expiry = self.get_future_date()
        self.test_user.memberprofile.club_expiry = self.get_future_date()
        self.test_user.memberprofile.medical_form_expiry = self.get_future_date()
        self.test_user.memberprofile.save()
        r = self.get_response()
        self.assertNotContains(r, self.test_user.first_name)#, html=True)
        self.assertNotContains(r, self.test_user.last_name)#, html=True)


class BulkAddFormsTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:BulkAddForms'
    view = BulkAddForms
    template_name = 'members_bulk_select.html'
    # TODO test a bulk operation


class TokenInputAPITest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:tokeninput-json'
    view = BulkAddForms

    def setUp_test(self):
        self.test_user = self.create_a_user()

    def test_template_used(self):
        # Does not use template, disable
        pass

    # def test_content_type(self):
    #     r = self.get_response()
    #     self.assertEqual(r.content_type, 'application/json')

    def test_member_in(self):
        r = self.get_response()
        self.assertContains(r, json.dumps(self.test_user.get_full_name()))


class ReportsOverviewTest(AsGroupMixin, ViewTestMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:ReportsOverview'
    template_name = 'members_reports_overview.html'
