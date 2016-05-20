from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'About',
        'access': is_all,
        'items': (
            ('About xSACdb', 'fa fa-info-circle', 'xsd_about:AboutView', []),
            ('Database Officers', 'fa fa-shield', 'xsd_about:DatabaseOfficers', []),
        )
    },
    {
        'title': 'xSACdb Administration',
        'access': is_admin,
        'items': (
            # ('All Update Requests', 'fa fa-cogs', 'DjangoAdminWarning', []),
            # ('Assign Roles', 'fa fa-cogs', 'DjangoAdminWarning', []),
            # ('ApplicationTools', 'fa fa-cogs', 'DjangoAdminWarning', []),
            ('Django Backend', 'fa fa-cogs', 'xsd_about:DjangoAdminWarning', []),
        )
    },
)
