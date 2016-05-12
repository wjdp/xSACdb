from django.contrib import admin
from reversion.admin import VersionAdmin

from xsd_members.models import *

class MemberAdmin(VersionAdmin):
    pass
class MembershipTypeAdmin(VersionAdmin):
    pass
class MailingAdmin(VersionAdmin):
    pass

admin.site.register(MemberProfile, MemberAdmin)
admin.site.register(MembershipType, MembershipTypeAdmin)
# admin.site.register(Mailing, MailingAdmin)
