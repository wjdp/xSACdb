from __future__ import unicode_literals

import json

from django.http import HttpResponse

from models import MemberProfile
from xSACdb.roles.decorators import require_verified


@require_verified
def tokeninput_json(request):
    members = MemberProfile.objects.all()
    data = []
    for member in members:
        t = {"name": member.get_full_name(), "id": member.pk}
        data.append(t)
    json_data = json.dumps(data)
    js_version = "var data = " + json_data + ";"
    return HttpResponse(content=js_version, content_type='application/json')
