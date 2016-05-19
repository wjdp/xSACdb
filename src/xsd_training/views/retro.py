from django.shortcuts import get_object_or_404

from django.shortcuts import redirect

from django.views.generic import TemplateView

from django.core.urlresolvers import reverse_lazy

from xSACdb.roles.decorators import require_training_officer
from xSACdb.roles.mixins import RequireTrainingOfficer

from xsd_members.models import MemberProfile
from xsd_training.models import *
from xsd_training.forms import *

from django.forms.models import formset_factory

from xsd_members.bulk_select import get_bulk_members

class RetroAddLessons(RequireTrainingOfficer ,TemplateView):
    template_name = 'retro_add_lessons.html'
    qualification = None
    trainee = None
    formsets = None
    all_valid = False

    def get_trainee_select_form(self):
        if self.request.GET and 'trainee' in self.request.GET:
            return TraineeSelectForm(self.request.GET)
        else:
            return TraineeSelectForm()

    def make_initial_list(self, lessons):
        lst =[]
        for lesson in lessons:
            lst.append( {'lesson': lesson} )
        return lst

    def make_row_formset(self, trainee, qualification, mode, POST_data=None):
        lessons = qualification.lessons_by_mode(mode)
        initial_data = self.make_initial_list(lessons)
        formset_blank = formset_factory(TraineeLessonCompletionDateForm, extra = 0)
        if POST_data:
            formset = formset_blank(POST_data, prefix=mode)
        else:
            formset = formset_blank(initial=initial_data, prefix=mode)
        for lesson, form in zip(lessons, formset):
            form.lesson_data = lesson
            if PerformedLesson.objects.get_lessons(trainee=trainee, lesson=lesson, partially_completed = True):
                form.already_partial = True
            if PerformedLesson.objects.get_lessons(trainee=trainee, lesson=lesson, completed = True):
                form.already_completed = True
                if POST_data:
                    form.display = False

            if POST_data and form.is_valid() and form.cleaned_data['date']==None:
                form.display = False
        return formset


    def make_all_formsets(self, trainee, qualification):
        formsets = []
        for mode in Lesson.MODE_CHOICES:
            formsets.append(self.make_row_formset(trainee, qualification, mode[0]))
        return formsets

    def retrive_all_formsets(self, trainee, qualification, POST_data):
        formsets = []
        for mode in Lesson.MODE_CHOICES:
            formsets.append(self.make_row_formset(trainee, qualification, mode[0], POST_data))
        return formsets

    def get_context_data(self, **kwargs):
        context = super(RetroAddLessons, self).get_context_data(**kwargs)
        context['trainee_select_form'] = self.get_trainee_select_form()
        context['trainee'] = self.trainee
        context['qualification'] = self.qualification
        context['all_valid'] = self.all_valid

        if self.formsets:
            context['formsets'] = self.formsets

        return context

    def get(self, request, *args, **kwargs):
        trainee_select_form = self.get_trainee_select_form()
        if trainee_select_form.is_valid():
            self.trainee = trainee_select_form.cleaned_data['trainee']
            self.qualification = trainee_select_form.cleaned_data['qualification']
            self.formsets = self.make_all_formsets(self.trainee, self.qualification)
        return super(RetroAddLessons, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.trainee = MemberProfile.objects.get(pk=request.POST['trainee'])
        self.qualification = Qualification.objects.get(pk=request.POST['qualification'])
        self.formsets = self.retrive_all_formsets(self.trainee, self.qualification, request.POST)

        all_valid = True

        for formset in self.formsets:
            if not formset.is_valid():
                all_valid = False

        self.all_valid = all_valid

        if all_valid and 'save_now' in request.POST:
            for formset in self.formsets:
                for form in formset:
                    if form.display and form.is_valid():
                        new_pl = PerformedLesson()
                        new_pl.lesson = form.lesson_data
                        new_pl.trainee = self.trainee
                        new_pl.date = form.cleaned_data['date']
                        if form.cleaned_data['partially_completed']:
                            new_pl.partially_completed = True
                        else:
                            new_pl.completed = True
                        new_pl.public_notes = form.cleaned_data['public_notes']
                        new_pl.private_notes = form.cleaned_data['private_notes']
                        new_pl.save()
            return redirect(reverse_lazy('TraineeNotes', args=[self.trainee.pk]))


        return super(RetroAddLessons, self).get(request, *args, **kwargs)

