

from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from xSACdb.roles.mixins import RequireInstructor
from xsd_auth.permissions import RequireObjectPermission, RequireAllowed
from xsd_training.forms import *
from xsd_training.views.base import TraineeFormMixin, TraineeViewMixin


class LessonDetail(RequireAllowed, TraineeViewMixin, DetailView):
    model = Lesson
    permission = 'can_view'
    context_object_name = 'lesson'
    template_name = 'xsd_training/trainee/lesson_detail.html'

    def is_allowed(self, user):
        # Trainee may view their lessons
        if self.get_trainee().user == user:
            return True
        # Instructors and training officers may view all
        elif is_instructor(user) or is_training(user):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(LessonDetail, self).get_context_data(**kwargs)
        context['trainee'] = self.get_trainee()
        context['pls'] = self.get_object().get_pls(self.get_trainee())
        context['state'] = self.get_object().get_lesson_state(self.get_trainee())
        return context


class PerformedLessonFormMixin(TraineeFormMixin):
    def get_lesson(self):
        return Lesson.objects.get(pk=self.kwargs['l_pk'])

    def get_context_data(self, **kwargs):
        context = super(PerformedLessonFormMixin, self).get_context_data(**kwargs)
        context['lesson'] = self.get_lesson()
        return context

    def get_success_url(self):
        return '{}#{}'.format(reverse('xsd_training:TraineeNotes', kwargs={'pk': self.kwargs['t_pk']}),
                              self.kwargs['l_pk'])


class PerformedLessonCreate(RequireInstructor, PerformedLessonFormMixin, CreateView):
    model = PerformedLesson
    template_name = 'xsd_training/trainee/pl_form.html'
    fields = ['date', 'instructor', 'completed', 'partially_completed', 'public_notes',
              'private_notes', ]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trainee = self.get_trainee()
        self.object.lesson = self.get_lesson()

        messages.add_message(self.request, messages.SUCCESS,
                             '{} added to {}'.format(self.object.lesson, self.get_trainee().full_name))

        return super(PerformedLessonCreate, self).form_valid(form)


class PerformedLessonUpdate(RequireObjectPermission, PerformedLessonFormMixin, UpdateView):
    model = PerformedLesson
    permission = 'can_edit'
    template_name = 'xsd_training/trainee/pl_form.html'
    fields = ['session', 'date', 'instructor', 'completed', 'partially_completed', 'public_notes',
              'private_notes', ]


class PerformedLessonDelete(RequireObjectPermission, PerformedLessonFormMixin, DeleteView):
    model = PerformedLesson
    permission = 'can_delete'

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR,
                             '{} removed from {}'.format(self.get_lesson(), self.get_trainee().full_name))
        return super(PerformedLessonDelete, self).delete(request, args, kwargs)
