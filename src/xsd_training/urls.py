from __future__ import unicode_literals

from django.conf.urls import url

from xsd_frontend.versioning import VersionHistoryView
from xsd_training.models import TraineeGroup, PerformedSDC, Session
from xsd_training.views import sessions, sdc, traineegroups, instructor, retro, support, trainee

urlpatterns = [
    url(r'^$', trainee.overview, name='training-overview'),
    url(r'^lessons/$', trainee.lessons, name='training-lessons'),
    url(r'^lessons/(?P<id>\d+)/$', trainee.lesson_detail, name='lesson_detail'),

    url(r'^feedback$', trainee.all_feedback, name='all-feedback'),

    url(r'^session/new/$', sessions.SessionCreate.as_view(), name='SessionCreate'),
    url(r'^session/list/$', sessions.SessionList.as_view(), name='SessionList'),
    url(r'^session/(?P<pk>\d+)/$', sessions.SessionPlanner.as_view(), name='SessionPlanner'),
    url(r'^session/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='SessionHistory',
        kwargs={'model': Session}),
    url(r'^session/(?P<pk>\d+)/action/(?P<action>\w+)/$', sessions.SessionAction.as_view(), name='SessionAction'),
    url(r'^session/(?P<pk>\d+)/complete/$', sessions.SessionComplete.as_view(), name='SessionComplete'),
    url(r'^session/(?P<pk>\d+)/delete/$', sessions.SessionDelete.as_view(), name='SessionDelete'),

    url(r'^pool-sheet/$', sessions.pool_sheet, name='PoolSheet'),
    url(r'^pool-sheet/generate$', sessions.pool_sheet_generate, name='PoolSheetGenerate'),

    url(r'^retro/lessons/$', retro.RetroAddLessons.as_view(), name='RetroAddLessons'),

    url(r'^teaching/upcoming/$', instructor.InstructorUpcoming, name='InstructorUpcoming'),

    url(r'^trainee/search/$', instructor.TraineeNotesSearch.as_view(), name='TraineeNotesSearch'),
    url(r'^trainee/(?P<pk>\d+)/$', instructor.TraineeNotes.as_view(), name='TraineeNotes'),
    url(r'^trainee/(?P<t_pk>\d+)/lesson/(?P<pk>\d+)/$', instructor.LessonDetail.as_view(), name='TraineeLessonDetail'),
    url(r'^trainee/(?P<pk>\d+)/set/$', instructor.trainee_notes_set, name='TraineeNotesSet'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/new/$', instructor.QualificationCreate.as_view(),
        name='TraineeQualificationCreate'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/(?P<pk>\d+)/$', instructor.QualificationUpdate.as_view(),
        name='TraineeQualificationUpdate'),
    url(r'^trainee/(?P<t_pk>\d+)/qualification/(?P<pk>\d+)/delete/$', instructor.QualificationDelete.as_view(),
        name='TraineeQualificationDelete'),

    url(r'^sdc/$', sdc.SDCList.as_view(), name='SDCList'),
    url(r'^sdc/reg-interest/$', sdc.sdc_register_interest, name='sdc_register_interest'),

    url(r'^sdc/plan/$', sdc.PerformedSDCCreate.as_view(), name='PerformedSDCCreate'),
    url(r'^sdc/upcoming/$', sdc.PerformedSDCList.as_view(), name='PerformedSDCList'),
    url(r'^sdc/(?P<pk>\d+)/$', sdc.PerformedSDCDetail.as_view(), name='PerformedSDCDetail'),
    url(r'^sdc/(?P<pk>\d+)/edit/$', sdc.PerformedSDCUpdate.as_view(), name='PerformedSDCUpdate'),
    url(r'^sdc/(?P<pk>\d+)/edit/action/(?P<action>\w+)/$', sdc.PerformedSDCAction.as_view(), name='PerformedSDCAction'),
    url(r'^sdc/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='PerformedSDCHistory',
        kwargs={'model': PerformedSDC}),
    url(r'^sdc/(?P<pk>\d+)/complete/$', sdc.PerformedSDCComplete.as_view(), name='PerformedSDCComplete'),
    url(r'^sdc/(?P<pk>\d+)/delete/$', sdc.PerformedSDCDelete.as_view(), name='PerformedSDCDelete'),
    url(r'^sdc/award/$', sdc.SDCAward, name='SDCAward'),

    url(r'^groups/$', traineegroups.TraineeGroupList.as_view(), name='TraineeGroupList'),
    url(r'^groups/new/$', traineegroups.TraineeGroupCreate.as_view(), name='TraineeGroupCreate'),
    url(r'^groups/(?P<pk>\d+)/$', traineegroups.TraineeGroupUpdate.as_view(), name='TraineeGroupUpdate'),
    url(r'^groups/(?P<pk>\d+)/history/$', VersionHistoryView.as_view(), name='TraineeGroupHistory',
        kwargs={'model': TraineeGroup}),
    url(r'^groups/(?P<pk>\d+)/action/(?P<action>\w+)/$', traineegroups.TraineeGroupAction.as_view(),
        name='TraineeGroupAction'),
    url(r'^groups/(?P<pk>\d+)/delete/$', traineegroups.TraineeGroupDelete.as_view(), name='TraineeGroupDelete'),

    url(r'^groups/progress/$', traineegroups.TraineeGroupProgress.as_view(), name='TraineeGroupProgress'),

    url(r'^update-requests/$', support.TrainingUpdateRequestList.as_view(), name='TrainingUpdateRequestList'),
    url(r'^update-requests/save/$', support.TrainingUpdateRequestRespond.as_view(),
        name='TrainingUpdateRequestRespond'),
]
