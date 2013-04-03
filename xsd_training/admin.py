from django.contrib import admin
from xsd_training.models import *


class PerformedLessonAdmin(admin.ModelAdmin):
    pass

class LessonAdmin(admin.ModelAdmin):
    pass

class QualificationAdmin(admin.ModelAdmin):
    pass

class SDCAdmin(admin.ModelAdmin):
    pass

class SessionAdmin(admin.ModelAdmin):
    pass

admin.site.register(PerformedLesson, PerformedLessonAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(SDC, SDCAdmin)
admin.site.register(Session, SessionAdmin)
