from django.contrib import admin
from reversion.admin import VersionAdmin

from xsd_sites.models import *

class SiteAdmin(VersionAdmin):
    pass

admin.site.register(Site, SiteAdmin)
