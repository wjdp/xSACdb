from django.conf.urls import patterns, include, url
from django.conf import settings
from xsd_training.views import sessions, sdc, traineegroups, instructor, retro, support

urlpatterns = patterns('',
    url(r'^$', 'xsd_training.views.trainee.overview', name='training-overview')    ,
    url(r'^lessons/$', 'xsd_training.views.trainee.lessons', name='training-lessons')    ,
    url(r'^lessons/(?P<id>\d+)/$', 'xsd_training.views.trainee.lesson_detail', name='lesson_detail'),
    url(r'^feedback$', 'xsd_training.views.trainee.all_feedback'),

    url(r'^pl-mouseover/$',support.PerformedLessonDetailMouseover.as_view(), name='PerformedLessonDetailMouseover'),
    url(r'^pl-mouseover-api/$',support.PerformedLessonDetailAPI.as_view(), name='PerformedLessonDetailAPI'),

    url(r'^session/new/$', sessions.SessionCreate.as_view(), name='SessionCreate'),
    url(r'^session/list/$', sessions.SessionList.as_view(), name='SessionList'),
    url(r'^session/(?P<pk>\d+)/$', sessions.SessionPlanner.as_view(), name='SessionPlanner'),
    url(r'^session/(?P<pk>\d+)/complete/$', sessions.SessionComplete.as_view(), name='SessionComplete'),
    url(r'^session/(?P<pk>\d+)/delete/$', sessions.SessionDelete.as_view(), name='SessionDelete'),

    url(r'^pool-sheet/$', 'xsd_training.views.sessions.pool_sheet', name='PoolSheet'),
    url(r'^pool-sheet/generate$', 'xsd_training.views.sessions.pool_sheet_generate', name='PoolSheetGenerate'),

    url(r'^retro/lessons/$', retro.RetroAddLessons.as_view(), name='RetroAddLessons'),

    url(r'^qualification/award/$', 'xsd_training.views.qualification.QualificationAward', name='QualificationAward'),

    url(r'^teaching/upcoming/$', 'xsd_training.views.instructor.InstructorUpcoming', name='InstructorUpcoming'),
    url(r'^teaching/notes/$', 'xsd_training.views.instructor.TraineeNotesSearch', name='TraineeNotesSearch'),
    url(r'^teaching/notes/(?P<pk>\d+)/$', instructor.TraineeNotes.as_view(), name='TraineeNotes'),

    url(r'^sdcs/$', sdc.SDCList.as_view(), name='SDCList'),
    url(r'^sdcs/reg-interest/$', 'xsd_training.views.sdc.sdc_register_interest', name='sdc_register_interest'),

    url(r'^sdcs/plan/$', sdc.PerformedSDCCreate.as_view(), name='PerformedSDCCreate'),
    url(r'^sdcs/upcoming/$', sdc.PerformedSDCList.as_view(), name='PerformedSDCList'),
    url(r'^sdcs/(?P<pk>\d+)/$', sdc.PerformedSDCDetail.as_view(), name='PerformedSDCDetail'),
    url(r'^sdcs/(?P<pk>\d+)/edit/$', sdc.PerformedSDCUpdate.as_view(), name='PerformedSDCUpdate'),
    url(r'^sdcs/(?P<pk>\d+)/complete/$', sdc.PerformedSDCComplete.as_view(), name='PerformedSDCComplete'),
    url(r'^sdcs/(?P<pk>\d+)/delete/$', sdc.PerformedSDCDelete.as_view(), name='PerformedSDCDelete'),

    url(r'^groups/$', traineegroups.TraineeGroupList.as_view(), name='TraineeGroupList'),
    url(r'^groups/new/$', traineegroups.TraineeGroupCreate.as_view(), name='TraineeGroupCreate'),
    url(r'^groups/(?P<pk>\d+)/$', traineegroups.TraineeGroupUpdate.as_view(), name='TraineeGroupUpdate'),
    url(r'^groups/(?P<pk>\d+)/delete/$', traineegroups.TraineeGroupDelete.as_view(), name='TraineeGroupDelete'),

    url(r'^groups/progress/$', traineegroups.TraineeGroupProgress.as_view(), name='TraineeGroupProgress'),

    url(r'^update-requests/$', support.TrainingUpdateRequestList.as_view(), name='TrainingUpdateRequestList'),
    url(r'^update-requests/save/$', support.TrainingUpdateRequestRespond.as_view(), name='TrainingUpdateRequestRespond'),


)



