from django.contrib import admin
from reversion.admin import VersionAdmin

from xsd_training.models import *


class PerformedLessonAdmin(VersionAdmin):
    pass

class LessonAdmin(VersionAdmin):
    fieldsets = (('Basic Info', {'fields': ('qualification','code','title','mode','order','required','description')}),
                 ('Practical Details', {'fields': ('max_depth','activities')}))
    list_display=('qualification','code','title','mode','order','required','max_depth')
    list_display_links=('code','title')
    list_filter=('qualification','mode')

class QualificationAdmin(VersionAdmin):
    list_display=('code', 'title','rank','instructor_qualification')
    list_filter=('instructor_qualification',)

class SDCAdmin(VersionAdmin):
    list_display=('title','min_qualification','category')
    list_filter=('min_qualification',)

class PerformedSDCAdmin(VersionAdmin):
    list_display=('sdc','datetime','completed')
    list_filter=('completed',)

class SessionAdmin(VersionAdmin):
    pass

class TraineeGroupAdmin(VersionAdmin):
    pass

admin.site.register(PerformedLesson, PerformedLessonAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(SDC, SDCAdmin)
admin.site.register(PerformedSDC, PerformedSDCAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(TraineeGroup, TraineeGroupAdmin)
