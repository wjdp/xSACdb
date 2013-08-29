from django.contrib import admin
from xsd_training.models import *


class PerformedLessonAdmin(admin.ModelAdmin):
    pass

class LessonAdmin(admin.ModelAdmin):
    fieldsets = (('Basic Info', {'fields': ('qualification','code','title','mode','order','required','description')}),
                 ('Practical Details', {'fields': ('max_depth','activities')}))
    list_display=('qualification','code','title','mode','order','required','max_depth')
    list_display_links=('code','title')
    list_filter=('qualification','mode')

class QualificationAdmin(admin.ModelAdmin):
    list_display=('title','rank','instructor_qualification') 
    list_filter=('instructor_qualification',)

class SDCAdmin(admin.ModelAdmin):
    list_display=('title','min_qualification')
    list_filter=('min_qualification',)

class PerformedSDCAdmin(admin.ModelAdmin):
    list_display=('sdc','datetime','completed')
    list_filter=('completed',)

class SessionAdmin(admin.ModelAdmin):
    pass

admin.site.register(PerformedLesson, PerformedLessonAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(SDC, SDCAdmin)
admin.site.register(PerformedSDC, PerformedSDCAdmin)
admin.site.register(Session, SessionAdmin)
