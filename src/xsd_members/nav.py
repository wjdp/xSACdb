from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Personal',
        'access': is_all,
        'items': (
            ('Your Profile', 'fa fa-user', 'xsd_members:my-profile', []),
        )
    },
    {
        'title': 'Current Membership',
        'access': is_members,
        'items': (
            ('Search', 'fa fa-search', 'xsd_members:MemberSearch', []),
            ('Members Listing', 'fa fa-th-list', 'xsd_members:MemberList', []),
        )
    },
    {
        'title': 'Records Needing Attention',
        'access': is_members,
        'items': (
            ('New Members', 'fa fa-flag', 'xsd_members:NewMembers', []),
            ('Update Requests', 'fa fa-envelope-o', 'xsd_members:MemberUpdateRequestList', []),
            ('Members With Blank Fields', 'fa fa-ban', 'xsd_members:MembersMissingFieldsList', []),
            ('Members With Expired Forms', 'fa fa-exclamation-triangle', 'xsd_members:MembersExpiredFormsList', []),
        )
    },
    {
        'title': 'Bulk Jobs',
        'access': is_members,
        'items': (
            ('Add Forms', 'fa fa-plus', 'xsd_members:BulkAddForms', []),
        )
    },
    {
        'title': 'Reporting',
        'access': is_members,
        'items': (
            ('Membership Overview', 'fa fa-bar-chart-o', 'xsd_members:ReportsOverview', []),
        )
    },
)
