from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from xsd_members.models import *

class MemberAdmin(CompareVersionAdmin):
    pass
class MembershipTypeAdmin(CompareVersionAdmin):
    pass

admin.site.register(MemberProfile, MemberAdmin)
admin.site.register(MembershipType, MembershipTypeAdmin)
