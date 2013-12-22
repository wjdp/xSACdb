from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    url(r'^$', 'xsd_training.views.overview', name='training-overview')    ,
    url(r'^lessons/all$', 'xsd_training.views.lessons', name='training-lessons')    ,
    url(r'^lesson/(?P<id>.*)$', 'xsd_training.views.lesson_detail', name='lesson_detail'),
    url(r'^feedback$', 'xsd_training.views.all_feedback'),

    url(r'^session/new/$', SessionCreate.as_view(), name='SessionCreate'),
    url(r'^session/list/$', SessionList.as_view(), name='SessionList'),
    url(r'^session/(?P<pk>\d+)/$', SessionPlanner.as_view(), name='SessionPlanner'),
    url(r'^session/(?P<pk>\d+)/delete/$', SessionDelete.as_view(), name='SessionDelete'),

    url(r'^qualification/award/$', 'xsd_training.views.QualificationAward', name='QualificationAward'),

    url(r'^teaching/upcoming/$', 'xsd_training.views.InstructorUpcoming', name='InstructorUpcoming'),
    url(r'^teaching/notes/$', 'xsd_training.views.TraineeNotesSearch', name='TraineeNotesSearch'),
    url(r'^teaching/notes/(?P<pk>\d+)/$', 'xsd_training.views.TraineeNotes', name='TraineeNotes'),

    url(r'^sdcs/$', SDCList.as_view(), name='SDCList'),
    url(r'^sdcs/reg-interest/$', 'xsd_training.views.sdc_register_interest', name='sdc_register_interest'),

    url(r'^sdcs/plan/$', PerformedSDCCreate.as_view(), name='PerformedSDCCreate'),
    url(r'^sdcs/upcoming/$', PerformedSDCList.as_view(), name='PerformedSDCList'),
    url(r'^sdcs/(?P<pk>\d+)/$', PerformedSDCDetail.as_view(), name='PerformedSDCDetail'),
    url(r'^sdcs/(?P<pk>\d+)/edit/$', PerformedSDCUpdate.as_view(), name='PerformedSDCUpdate'),
    url(r'^sdcs/(?P<pk>\d+)/complete/$', PerformedSDCComplete.as_view(), name='PerformedSDCComplete'),
    url(r'^sdcs/(?P<pk>\d+)/delete/$', PerformedSDCDelete.as_view(), name='PerformedSDCDelete'),

    url(r'^groups/$', TraineeGroupList.as_view(), name='TraineeGroupList'),
    url(r'^groups/new/$', TraineeGroupCreate.as_view(), name='TraineeGroupCreate'),
    url(r'^groups/(?P<pk>\d+)/$', TraineeGroupUpdate.as_view(), name='TraineeGroupUpdate'),
    url(r'^groups/(?P<pk>\d+)/delete/$', TraineeGroupDelete.as_view(), name='TraineeGroupDelete'),

)



