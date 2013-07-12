from tastypie.resources import Resource, ModelResource
from tastypie import fields, utils

from models import MemberProfile
from django.contrib.auth.models import User

from django.http import HttpResponse

import json

class UserResource(ModelResource):
    class Meta:
        queryset=User.objects.all()
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
        queryset=User.objects.all()
        data=[]
        for user in queryset:
            t=TokenInputUser()
            t.id=user.pk
            t.name=user.first_name + " " + user.last_name
            data.append(t)
        return data

    def obj_get_list(self, request = None, **kwargs):
        return self.get_object_list(request)

    class Meta:
        resource_name='tokeninput_members'
        object_class=TokenInputUser


def tokeninput_json(request):
    users=User.objects.all()
    data=[]
    for user in users:
        t={"id":user.pk, "name":user.get_full_name()}
        data.append(t)
    json_data=json.dumps(data)
    return HttpResponse(content=json_data, mimetype='application/json')