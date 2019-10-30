from django.contrib import admin
from .models import *


class KitAdmin(admin.ModelAdmin):
    pass
class LoanAdmin(admin.ModelAdmin):
    pass

admin.site.register(Kit, KitAdmin)
admin.site.register(Loan, LoanAdmin)
