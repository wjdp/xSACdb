from models import MemberProfile

import StringIO
import csv

TOKEN_NAME = 'names'


def get_some_objects(list):
    return MemberProfile.objects.filter(pk__in=list)


def parse_token_data(request_post):
    f = StringIO.StringIO(request_post[TOKEN_NAME])
    reader = csv.reader(f, delimiter=',')
    user_ids = []
    for row in reader:
        user_ids = row
    return user_ids


def get_bulk_members(request):
    user_ids = parse_token_data(request.POST)
    members = get_some_objects(user_ids)
    return members
