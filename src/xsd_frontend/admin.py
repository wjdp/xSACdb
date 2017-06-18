from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

admin.site.site_title = '[xSACdb:{club_name}]'.format(club_name=settings.CLUB.get('name'))
admin.site.site_header = admin.site.site_title
