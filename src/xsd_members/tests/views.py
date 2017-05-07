from __future__ import unicode_literals
import json

from xSACdb.test_helpers import BaseTest, ViewTestMixin, AsGroupMixin
from xSACdb.roles.groups import GROUP_MEMBERS
from xsd_members.views import *


class ProfileViewTest(ViewTestMixin, BaseTest):
    url_name = 'xsd_members:my-profile'
    template_name = 'xsd_members/member/detail.html'
    allowed_unverified = True


class ProfileEditViewTest(ViewTestMixin, BaseTest):
    url_name = 'xsd_members:MyProfileEdit'
    view = MyProfileEdit
    allowed_unverified = True


class MemberSearchTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberSearch'
    view = MemberSearch

    def test_search(self):
        # Do search for user, ensure user's name is in response
        u = self.create_a_user()
        c = self.get_client()
        r = c.get("{}?q={}".format(
            self.get_url(),
            u.last_name,
        ))
        self.assertEqual(200, r.status_code)
        self.assertContains(r, u.first_name)#, html=True)
        self.assertContains(r, u.last_name)#, html=True)


class MemberDetailTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberDetail'
    view = MemberDetail

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()
        cls.url_kwargs = {'pk': cls.test_user.memberprofile.pk}

    def test_member_detail(self):
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#


class MemberEditTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberEdit'
    view = MemberEdit

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()
        cls.url_kwargs = {'pk': cls.test_user.memberprofile.pk}

    def test_member_detail(self):
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

        # TODO perform an edit


class MemberDeleteTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberDelete'
    view = MemberDelete

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()
        cls.url_kwargs = {'pk': cls.test_user.memberprofile.pk}
        cls.test_user_pk = cls.test_user.pk

    def test_member_in_page(self):
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_delete(self):
        self.assertEqual(MemberProfile.objects.filter(pk=self.test_user_pk).count(), 1)
        self.get_client().post(self.get_url())
        self.assertEqual(MemberProfile.objects.filter(pk=self.test_user_pk).count(), 0)


class MemberArchiveTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberArchive'
    view = MemberArchive

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()
        cls.url_kwargs = {'pk': cls.test_user.memberprofile.pk}

    def test_member_in_page(self):
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_archive(self):
        self.assertFalse(self.test_user.memberprofile.archived)
        self.get_client().post(self.get_url())
        self.test_user.memberprofile.refresh_from_db()
        self.assertTrue(self.test_user.memberprofile.archived)


class MemberListTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MemberList'
    view = MemberList

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()

    def test_member_in_list(self):
        """Current members should show in the list"""
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_member_not_in_list(self):
        """The current members list should not show archived members"""
        self.test_user.memberprofile.archive(self.user)
        self.test_user.memberprofile.save()
        r = self.get_response()
        self.assertNotContains(r, self.test_user.first_name)#, html=True)
        self.assertNotContains(r, self.test_user.last_name)#, html=True)


class NewMembersTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:NewMembers'
    view = NewMembers

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()

    def test_member_in_list(self):
        r = self.response
        self.assertContains(r, self.test_user.first_name)#, html=True)
        self.assertContains(r, self.test_user.last_name)#, html=True)

    def test_member_not_in_list(self):
        self.test_user.memberprofile.new_notify = False
        self.test_user.memberprofile.save()
        r = self.get_response()
        self.assertNotContains(r, self.test_user.first_name)#, html=True)
        self.assertNotContains(r, self.test_user.last_name)#, html=True)


class MembersExpiredFormsListTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MembersExpiredFormsList'
    view = MembersExpiredFormsList

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()

    def test_member_in_list(self):
        r = self.response
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

class MembersArchivedList(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:MembersArchivedList'
    view = MembersArchivedList

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()

    def test_member_in_list(self):
        """Archived members should show in MembersArchivedList"""
        self.test_user.memberprofile.archive(self.user)
        self.test_user.memberprofile.save()
        r = self.get_response()
        self.assertContains(r, self.test_user.first_name)  # , html=True)
        self.assertContains(r, self.test_user.last_name)  # , html=True)

    def test_member_not_in_list(self):
        """Current members should not show in MembersArchivedList"""
        r = self.response
        self.assertNotContains(r, self.test_user.first_name)  # , html=True)
        self.assertNotContains(r, self.test_user.last_name)  # , html=True)


class BulkAddFormsTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:BulkAddForms'
    view = BulkAddForms
    template_name = 'members_bulk_select.html'
    # TODO test a bulk operation


class TokenInputAPITest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:tokeninput-json'
    view = BulkAddForms

    @classmethod
    def setUp_test(cls):
        cls.test_user = cls.create_a_user()

    def test_template_used(self):
        # Does not use template, disable
        pass

    # def test_content_type(self):
    #     r = self.get_response()
    #     self.assertEqual(r.content_type, 'application/json')

    def test_member_in(self):
        r = self.response
        self.assertContains(r, json.dumps(self.test_user.get_full_name()))


class ReportsOverviewTest(ViewTestMixin, AsGroupMixin, BaseTest):
    GROUPS = [GROUP_MEMBERS]
    url_name = 'xsd_members:ReportsOverview'
    template_name = 'members_reports_overview.html'
