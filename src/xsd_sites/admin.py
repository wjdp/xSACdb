from django.contrib import admin
from xsd_sites.models import *

class SiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Site, SiteAdmin)
