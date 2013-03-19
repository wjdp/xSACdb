from django.contrib import admin
from xsd_members.models import *

class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(MemberProfile, MemberAdmin)
