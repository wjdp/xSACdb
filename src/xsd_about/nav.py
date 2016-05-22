from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'About',
        'access': is_all,
        'items': [
            ('About xSACdb', None, 'fa fa-info-circle', 'xsd_about:AboutView', []),
            ('Database Officers', None, 'fa fa-shield', 'xsd_about:DatabaseOfficers', []),
        ]
    },
    {
        'title': 'xSACdb Administration',
        'access': is_admin,
        'items': [
            # ('All Update Requests', None, 'fa fa-cogs', 'DjangoAdminWarning', []),
            # ('Assign Roles', None, 'fa fa-cogs', 'DjangoAdminWarning', []),
            # ('ApplicationTools', None, 'fa fa-cogs', 'DjangoAdminWarning', []),
            ('Django Backend', None, 'fa fa-cogs', 'xsd_about:DjangoAdminWarning', []),
        ]
    },
)
