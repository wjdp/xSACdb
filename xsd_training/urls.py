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

)



