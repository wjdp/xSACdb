from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Account Settings',
        'access': is_all,
        'items': (
            ('Change Password', 'fa fa-key', 'xsd_auth:account_change_password', []),
            ('Social Login', 'fa fa-facebook-square', 'xsd_auth:socialaccount_connections', []),
        )
    },
)
