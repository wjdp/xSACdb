from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Trips',
        'access': is_verified,
        'items': [
            ('Upcoming', None, 'fa fa-calendar', 'xsd_trips:TripListUpcoming', []),
            ('Past', None, 'fa fa-calendar-times-o', 'xsd_trips:TripListArchive', []),
        ]
    },
    {
        'title': 'Organise',
        'access': is_verified,
        'items': [
            ('My Trips', None, 'fa fa-suitcase', 'xsd_trips:TripCreate', []),
        ]
    },
    {
        'title': 'Administration',
        'access': is_trips,
        'items': [
            ('Needing Approval', None, 'fa fa-calendar-plus-o', 'xsd_trips:TripCreate', []),
        ]
    },
)
