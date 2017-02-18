from __future__ import unicode_literals

import decimal
import random

from datetime import timedelta, datetime
from .states import *

TRIP_NAME_PREFIX1 = (
    'Outer',
    'Inner',
    'Slightly',
    'Downright',
    'Hairy',
    'Moisture',
    'Navelint',
    'Bootjuice',
    'Widdly',
    'Waddly',
    'Rather',
    'Wester',
    'Light',
    'Ice',
    'Stone',
    'Nude',
    'Butter',
    'Cheese',
    'Cheddar',
    'Bishop',
    'Stink',
    'Cliff',
    'Wilde',
    'Water',
    'Haunt',
)

TRIP_NAME_PREFIX2 = (
    'muddy',
    'miserable',
    '-ridden',
    '-rife',
    'fliddle',
    'steep',
    'meadow',
    'ston',
    'wall',
    'wheat',
    'well',
    'loch',
    'mill',
    'ston',
    'ness',
    'bush',
    'goat',
)

TRIP_NAME_SUFFIXES = (
    'Coast',
    'Island',
    'Aquarium',
    'Creek',
    'Bay',
    'Falls',
    'Lagoon',
    'Flow',
    'Lakes',
    'Tavern',
    'Puddle',
    'Water',
    'Gulf'
)

def generate_fake_name():
    return "{}{} {}".format(
        random.choice(TRIP_NAME_PREFIX1),
        random.choice(TRIP_NAME_PREFIX2),
        random.choice(TRIP_NAME_SUFFIXES),
    )


class TripFakeDataMixin(object):

    def fake(self, fake, quals, past=False):
        self.name = generate_fake_name()
        if past:
            self.date_start = fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None).date()
        else:
            self.date_start = fake.date_time_between(start_date="now", end_date="+2y", tzinfo=None).date()

        self.date_end = fake.date_time_between(
            start_date=self.date_start + timedelta(days=1),
            end_date=self.date_start + timedelta(days=14),
            tzinfo=None
        ).date()

        if fake.boolean(chance_of_getting_true=10):
            self.cost = decimal.Decimal(random.randrange(100000))/100
        else:
            self.cost = random.randrange(900) + 50

        self.spaces = random.randrange(4, 128)

        if fake.boolean(chance_of_getting_true=95):
            self.description = '\n\n'.join(fake.paragraphs(nb=random.randrange(1, 4)))

        if fake.boolean(chance_of_getting_true=90):
            if fake.boolean(chance_of_getting_true=40):
                # OD Trip
                self.max_depth = random.randrange(1, 20)
                self.min_qual = quals[0]
            elif fake.boolean(chance_of_getting_true=40):
                # SD Trip
                self.max_depth = random.randrange(1, 35)
                self.min_qual = quals[1]
            elif fake.boolean(chance_of_getting_true=40):
                # DL+ Trip
                self.max_depth = random.randrange(1, 50)
                self.min_qual = quals[2]

        if past:
            if fake.boolean(chance_of_getting_true=90):
                if self.date_end > (datetime.now() - timedelta(hours=24*365)).date() and \
                        fake.boolean(chance_of_getting_true=30):
                    self.state = STATE_CLOSED
                elif fake.boolean(chance_of_getting_true=20):
                    self.state = STATE_CANCELLED
                else:
                    self.state = STATE_COMPLETED
            else:
                # Cancelled
                self.state = STATE_CANCELLED
        else:
            self.state = random.choice((
                STATE_DENIED,
                STATE_NEW,
                STATE_APPROVED,
                STATE_CANCELLED,
                STATE_OPEN,
                STATE_CLOSED,
            ))


