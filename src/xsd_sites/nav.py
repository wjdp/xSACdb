from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Sites',
        'access': is_all,
        'items': [
            ('Overview', None, 'fa fa-map-marker', 'xsd_sites:SitesOverview', []),
            # ('Search', None, 'fa fa-tachometer', 'xsd_sites:SitesOverview', []),
        ]
    },
    {
        'title': 'Sites Administration',
        'access': is_sites,
        'items': [
            ('Add Site', None, 'fa fa-plus', 'xsd_sites:SiteCreate', []),
            ('Edit Sites', None, 'fa fa-pencil', 'xsd_sites:SitesList', []),
        ]
    },
)
