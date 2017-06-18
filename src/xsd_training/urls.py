from __future__ import unicode_literals

from django.conf.urls import url

from xsd_frontend.versioning import VersionHistoryView
from xsd_training.views import *

urlpatterns = [
    url(r'^$', trainee.overview, name='training-overview'),
    url(r'^lessons/$', trainee.lessons, name='training-lessons'),
    url(r'^lessons/(?P<id>\d+)/$', trainee.lesson_detail, name='lesson_detail'),

    url(r'^feedback$', trainee.all_feedback, name='all-feedback'),

    url(r'^session/new/$', SessionCreate.as_view(), name='SessionCreate'),
    url(r'^session/list/$', SessionList.as_view(), name='SessionList'),
    url(r'^session/(?P<pk>\d+)/$', SessionPlanner.as_view(), name='SessionPlanner'),
    url(r'^session/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='SessionHistory',
        kwargs={'model': Session}),
    url(r'^session/(?P<pk>\d+)/action/(?P<action>\w+)/$', SessionAction.as_view(), name='SessionAction'),
    url(r'^session/(?P<pk>\d+)/complete/$', SessionComplete.as_view(), name='SessionComplete'),
    url(r'^session/(?P<pk>\d+)/delete/$', SessionDelete.as_view(), name='SessionDelete'),

    url(r'^pool-sheet/$', pool_sheet, name='PoolSheet'),
    url(r'^pool-sheet/generate$', pool_sheet_generate, name='PoolSheetGenerate'),

    url(r'^retro/lessons/$', RetroAddLessons.as_view(), name='RetroAddLessons'),

    url(r'^teaching/upcoming/$', InstructorUpcoming, name='InstructorUpcoming'),

    url(r'^trainee/search/$', TraineeNotesSearch.as_view(), name='TraineeNotesSearch'),
    url(r'^trainee/(?P<pk>\d+)/$', TraineeNotes.as_view(), name='TraineeNotes'),
    url(r'^trainee/(?P<t_pk>\d+)/lesson/(?P<pk>\d+)/$', LessonDetail.as_view(), name='TraineeLessonDetail'),
    url(r'^trainee/(?P<t_pk>\d+)/lesson/(?P<l_pk>\d+)/new/$', PerformedLessonCreate.as_view(), name='TraineePerformedLessonCreate'),
    url(r'^trainee/(?P<t_pk>\d+)/lesson/(?P<l_pk>\d+)/(?P<pk>\d+)/$', PerformedLessonUpdate.as_view(), name='TraineePerformedLessonUpdate'),
    url(r'^trainee/(?P<t_pk>\d+)/lesson/(?P<l_pk>\d+)/(?P<pk>\d+)/delete/$', PerformedLessonDelete.as_view(), name='TraineePerformedLessonDelete'),
    url(r'^trainee/(?P<pk>\d+)/set/$', trainee_notes_set, name='TraineeNotesSet'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/new/$', QualificationCreate.as_view(),
        name='TraineeQualificationCreate'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/(?P<pk>\d+)/$', QualificationUpdate.as_view(),
        name='TraineeQualificationUpdate'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/(?P<pk>\d+)/delete/$', QualificationDelete.as_view(),
        name='TraineeQualificationDelete'),

    url(r'^sdc/$', SDCList.as_view(), name='SDCList'),
    url(r'^sdc/reg-interest/$', sdc_register_interest, name='sdc_register_interest'),

    url(r'^sdc/plan/$', PerformedSDCCreate.as_view(), name='PerformedSDCCreate'),
    url(r'^sdc/upcoming/$', PerformedSDCList.as_view(), name='PerformedSDCList'),
    url(r'^sdc/(?P<pk>\d+)/$', PerformedSDCDetail.as_view(), name='PerformedSDCDetail'),
    url(r'^sdc/(?P<pk>\d+)/edit/$', PerformedSDCUpdate.as_view(), name='PerformedSDCUpdate'),
    url(r'^sdc/(?P<pk>\d+)/edit/action/(?P<action>\w+)/$', PerformedSDCAction.as_view(), name='PerformedSDCAction'),
    url(r'^sdc/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='PerformedSDCHistory',
        kwargs={'model': PerformedSDC}),
    url(r'^sdc/(?P<pk>\d+)/complete/$', PerformedSDCComplete.as_view(), name='PerformedSDCComplete'),
    url(r'^sdc/(?P<pk>\d+)/delete/$', PerformedSDCDelete.as_view(), name='PerformedSDCDelete'),
    url(r'^sdc/award/$', SDCAward, name='SDCAward'),

    url(r'^groups/$', TraineeGroupList.as_view(), name='TraineeGroupList'),
    url(r'^groups/new/$', TraineeGroupCreate.as_view(), name='TraineeGroupCreate'),
    url(r'^groups/(?P<pk>\d+)/$', TraineeGroupUpdate.as_view(), name='TraineeGroupUpdate'),
    url(r'^groups/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='TraineeGroupHistory',
        kwargs={'model': TraineeGroup}),
    url(r'^groups/(?P<pk>\d+)/action/(?P<action>\w+)/$', TraineeGroupAction.as_view(),
        name='TraineeGroupAction'),
    url(r'^groups/(?P<pk>\d+)/delete/$', TraineeGroupDelete.as_view(), name='TraineeGroupDelete'),

    url(r'^groups/progress/$', TraineeGroupProgress.as_view(), name='TraineeGroupProgress'),

    url(r'^update-requests/$', TrainingUpdateRequestList.as_view(), name='TrainingUpdateRequestList'),
    url(r'^update-requests/save/$', TrainingUpdateRequestRespond.as_view(),
        name='TrainingUpdateRequestRespond'),
]
