from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Sites',
        'access': is_all,
        'items': (
            ('Overview', 'fa fa-map-marker', 'xsd_sites:SitesOverview', []),
            # ('Search', 'fa fa-tachometer', 'xsd_sites:SitesOverview', []),
        )
    },
    {
        'title': 'Sites Administration',
        'access': is_sites,
        'items': (
            ('Add Site', 'fa fa-plus', 'xsd_sites:SiteCreate', []),
            ('Edit Sites', 'fa fa-pencil', 'xsd_sites:SitesList', []),
        )
    },
)
