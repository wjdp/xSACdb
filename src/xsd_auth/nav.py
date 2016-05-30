from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Account Settings',
        'access': is_all,
        'items': [
            ('Change Password', None, 'fa fa-key', 'xsd_auth:account_change_password', ['xsd_auth:account_set_password']),
            ('Social Login', None, 'fa fa-facebook-square', 'xsd_auth:socialaccount_connections', []),
        ]
    },
    {
        'title': 'Session',
        'access': is_all,
        'items': [
            ('Logout', None, 'fa fa-sign-out', 'xsd_auth:account_logout', []),
        ]
    },
)
