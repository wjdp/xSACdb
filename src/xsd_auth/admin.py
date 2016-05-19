from django.contrib import admin

from xsd_auth.models import *

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

