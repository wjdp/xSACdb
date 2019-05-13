from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from reversion_compare.admin import CompareVersionAdmin

from xsd_training.models import *


class PerformedLessonAdmin(CompareVersionAdmin):
    list_display = ('uid', 'session', 'date', 'lesson', 'instructor', 'trainee', 'completed', 'partially_completed')
    list_filter = ('completed', 'partially_completed')


class LessonAdmin(ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields': ('qualification', 'code', 'title', 'mode', 'order', 'required', 'description')}),
        ('Practical Details', {'fields': ('max_depth', 'activities')}))
    list_display = ('qualification', 'code', 'title', 'mode', 'order', 'required', 'max_depth')
    list_display_links = ('code', 'title')
    list_filter = ('qualification', 'mode')


class PerformedQualificationAdmin(CompareVersionAdmin):
    list_display = ('uid', 'trainee', 'qualification', 'mode', 'xo_from', 'signed_off_on', 'signed_off_by', 'created')
    list_filter = ('qualification', 'mode')


class QualificationAdmin(ModelAdmin):
    list_display = ('code', 'title', 'rank', 'instructor_qualification', 'active')
    list_filter = ('instructor_qualification',)


class SDCAdmin(ModelAdmin):
    list_display = ('title', 'min_qualification', 'category')
    list_filter = ('min_qualification',)


class PerformedSDCAdmin(CompareVersionAdmin):
    list_display = ('uid', 'sdc', 'datetime', 'completed')
    list_filter = ('completed',)


class SessionAdmin(CompareVersionAdmin):
    list_display = ('uid', 'name', 'when', 'where', 'completed')
    list_filter = ('where', 'completed')


class TraineeGroupAdmin(CompareVersionAdmin):
    list_display = ('uid', 'name')


admin.site.register(PerformedLesson, PerformedLessonAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(PerformedQualification, PerformedQualificationAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(SDC, SDCAdmin)
admin.site.register(PerformedSDC, PerformedSDCAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(TraineeGroup, TraineeGroupAdmin)
