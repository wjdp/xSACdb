from .models import MemberProfile

import io
import csv

TOKEN_NAME = 'names'


def get_some_objects(list):
    return MemberProfile.objects.filter(pk__in=list)


def parse_token_data(request_post):
    f = io.StringIO(request_post[TOKEN_NAME])
    reader = csv.reader(f, delimiter=',')
    user_ids = []
    for row in reader:
        user_ids = set(row)
    return user_ids


def get_bulk_members(request, method="POST"):
    if method == "POST":
        user_ids = parse_token_data(request.POST)
    elif method == "GET":
        user_ids = parse_token_data(request.GET)
    else:
        raise ValueError("Unsupported method")

    members = get_some_objects(user_ids)
    return members
