from xSACdb.roles.functions import *
from django.conf import settings

NAV = (
    {
        'title': 'Home',
        'access': is_all,
        'items': [
            ('Dashboard', None, 'fa fa-tachometer', 'xsd_frontend:dashboard', []),
        ]
    },
)

APP_LIST = [
    {
        'title': 'Members',
        'access': is_all,
        'app': 'xsd_members',
        'url': 'xsd_members:my-profile',
        'icon': 'fa fa-user',
    },
    {
        'title': 'Training',
        'access': is_verified,
        'app': 'xsd_training',
        'url': 'xsd_training:training-overview',
        'icon': 'fa fa-mortar-board',
    },
    # {
    #     'title': 'Trips',
    #     'access': is_verified,
    #     'app': 'xsd_trips',
    #     'url': 'xsd_trips:TripList',
    #     'icon': 'fa fa-road',
    # },
    # {
    #     'title': 'Kit',
    #     'access': is_verified,
    #     'app': 'xsd_kit',
    #     'url': 'xsd_kit:KitOverview',
    #     'icon': 'fa fa-tags',
    # },
    {
        'title': 'Sites',
        'access': is_verified,
        'app': 'xsd_sites',
        'url': 'xsd_sites:SitesOverview',
        'icon': 'fa fa-map-marker',
    },
    {
        'title': 'About',
        'access': is_all,
        'app': 'xsd_about',
        'url': 'xsd_about:AboutView',
        'icon': 'fa fa-info-circle',
    },
    {
        'title': 'Account',
        'access': is_all,
        'app': 'xsd_auth',
        'url': '',
        'icon': 'fa fa-key',
    },
]
