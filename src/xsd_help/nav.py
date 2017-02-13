from xSACdb.roles.functions import is_all

NAV = (
    {
        'title': 'Help',
        'access': is_all,
        'items': [
            ('Documentation', None, 'fa fa-question', 'xsd_help:HelpView', []),
        ]
    },
)

