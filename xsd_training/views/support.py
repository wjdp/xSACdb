
from django.views.generic import DetailView, View

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
import json

from django.http import HttpResponse

from django.contrib.auth import get_user_model
from xsd_training.models import PerformedLesson, Lesson, Qualification
from xSACdb.roles.mixins import RequireInstructor, RequireTrainingOfficer

# This was slow, pretty sure it's no longer used
class PerformedLessonDetailMouseover(RequireInstructor, DetailView):
    model = PerformedLesson
    template_name = 'performedlesson_detail_mouseover.html'
    context_object_name = 'pls'
    lesson = None
    trainee = None
    is_completed = False
    is_partially_completed = False

    def get_object(self, queryset=None):
        if 't' in self.request.GET and 'l' in self.request.GET:
            U = get_user_model()
            self.trainee = U.objects.get(pk=self.request.GET['t'])
            self.lesson = Lesson.objects.get(pk=self.request.GET['l'])
            qs = PerformedLesson.objects.filter(trainee = self.trainee, lesson = self.lesson)
            if self.lesson.is_completed(self.trainee):
                self.is_completed = True
            if self.lesson.is_partially_completed(self.trainee):
                self.is_partially_completed = True
            return qs
    def get_context_data(self, **kwargs):
        context = super(PerformedLessonDetailMouseover, self).get_context_data(**kwargs)
        context['lesson'] = self.lesson
        context['trainee'] = self.trainee
        context['is_completed'] = self.is_completed
        context['is_partially_completed'] = self.is_partially_completed
        return context

# Provides data to JS in progress reports
class PerformedLessonDetailAPI(RequireInstructor, View):
    def get(self, request, *args, **kwargs):
        if 't' in self.request.GET:
            U = get_user_model()
            trainee = U.objects.get(pk=self.request.GET['t'])
            qualification = Qualification.objects.get(pk=self.request.GET['q'])

            lessons = Lesson.objects.filter(qualification = qualification)

            ret = {}

            for lesson in lessons:
                ret_lesson = {}
                pls = None
                if lesson.is_completed(trainee):
                    ret_lesson['state'] = 'completed'
                    pls = PerformedLesson.objects.filter(trainee = trainee, lesson = lesson, completed=True).order_by('date')[:1]
                elif lesson.is_partially_completed(trainee):
                    ret_lesson['state'] = 'partially_completed'
                    pls = PerformedLesson.objects.filter(trainee = trainee, lesson = lesson, partially_completed=True).order_by('date')[:1]
                else:
                    ret_lesson['state'] = 'not'
                ret_lesson['code'] = lesson.code
                ret_lesson['title'] = lesson.title
                ret_lesson['mode'] = lesson.mode
                if pls:
                    for pl in pls:
                        ret_lesson['pl'] = {
                                'session': str(pl.session),
                                'date': str(pl.date),
                                'instructor': str(pl.instructor),
                                'public_notes': str(pl.public_notes),
                                'private_notes': str(pl.private_notes),
                            }
                        if pl.instructor:
                            ret_lesson['pl']['instructor']=pl.instructor.get_full_name()


                ret[lesson.pk]=ret_lesson
            return HttpResponse(json.dumps(ret))

from xsd_frontend.base import BaseUpdateRequestList, BaseUpdateRequestRespond

class TrainingUpdateRequestList(RequireTrainingOfficer, BaseUpdateRequestList):
    template_name="training_update_request.html"
    area='tra'
    form_action=reverse_lazy('TrainingUpdateRequestRespond')
    custom_include='training_update_request_custom.html'

class TrainingUpdateRequestRespond(RequireTrainingOfficer, BaseUpdateRequestRespond):
    success_url=reverse_lazy('TrainingUpdateRequestList')
