from tastypie.resources import ModelResource

from models import MemberProfile


class MemberResource(ModelResource):
    class Meta:
        queryset = MemberProfile.objects.all()
        resource_name = 'members'
        allowed_methods = ['get']
