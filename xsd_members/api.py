from tastypie.resources import Resource, ModelResource
from tastypie import fields, utils

from models import MemberProfile
from django.contrib.auth import get_user_model

from django.http import HttpResponse

import json

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
        U = get_user_model()
        queryset=U.objects.all()
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
    U = get_user_model()
    users=U.objects.all()
    data=[]
    for user in users:
        t={"name":user.get_full_name(), "id":user.pk}
        data.append(t)
    json_data=json.dumps(data)
    js_version="var data = " + json_data + ";"
    return HttpResponse(content=js_version, mimetype='text/javascript')
