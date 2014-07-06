from django import template

from xsd_members.views import *

register = template.Library()

@register.simple_tag
def todo(item):
    if item == 'NewMembers':
        view = NewMembers()
        x= NewMembers.get_queryset(view).count()
        if x>0:
            return '<div class="pull-right badge">'+str(x)+'</div>'
        else: return ""
    if item == 'MemberUpdateRequestList':
        view = MemberUpdateRequestList()
        x= MemberUpdateRequestList.get_queryset(view).filter(completed=False, area='mem').count()
        print x
        if x>0:
            return '<div class="pull-right badge badge-important">'+str(x)+'</div>'
        else: return ""
    if item == 'MembersMissingFieldsList':
        view = MembersMissingFieldsList()
        x= MembersMissingFieldsList.get_queryset(view).count()
        if x>0:
            return '<div class="pull-right badge">'+str(x)+'</div>'
        else: return ""
    if item == 'MembersExpiredFormsList':
        view = MembersExpiredFormsList()
        x= MembersExpiredFormsList.get_queryset(view).count()
        if x>0:
            return '<div class="pull-right badge">'+str(x)+'</div>'
        else: return ""

