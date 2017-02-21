import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from tastypie import fields
from tastypie.resources import Resource, ModelResource

from models import MemberProfile
from xSACdb.roles.decorators import require_verified


class UserResource(ModelResource):
    class Meta:
        U = get_user_model()
        queryset=U.objects.all()
        resource_name='users'
        allowed_methods=['get']
        fields=['id','email','first_name','last_name','username']

class MemberResource(ModelResource):
    user = fields.ToOneField(UserResource,'user',full=True)

    class Meta:
        queryset = MemberProfile.objects.all()
        resource_name = 'members'
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        #bundle['name']=bundle
        return bundle

class TokenInputUser(object):
    id=None
    name=''

class TokenInputResource(Resource):
    id=fields.IntegerField(attribute='id')
    name=fields.CharField(attribute='name')

    def get_object_list(self, request):
        queryset = MemberProfile.objects.all()
        data = []
        for member in queryset:
            t = TokenInputUser()
            t.id = member.pk
            t.name = member.get_full_name
            data.append(t)
        return data

    def obj_get_list(self, request = None, **kwargs):
        return self.get_object_list(request)

    class Meta:
        resource_name='tokeninput_members'
        object_class=TokenInputUser

@require_verified
def tokeninput_json(request):
    members = MemberProfile.objects.all()
    data=[]
    for member in members:
        t={"name":member.get_full_name(), "id":member.pk}
        data.append(t)
    json_data=json.dumps(data)
    js_version="var data = " + json_data + ";"
    return HttpResponse(content=js_version, content_type='application/json')
