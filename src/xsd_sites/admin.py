from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from xsd_sites.models import *

class SiteAdmin(CompareVersionAdmin):
    pass

admin.site.register(Site, SiteAdmin)
