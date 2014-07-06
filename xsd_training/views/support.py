from django.views.generic import DetailView

from django.shortcuts import get_object_or_404

from xsd_training.models import PerformedLesson

class PerformedLessonDetailMouseover(DetailView):
	model = PerformedLesson
	template_name = 'performedlesson_detail_mouseover.html'
	context_object_name = 'pl'

	def get_object(self, queryset=None):
		if 'pl' in self.request.GET:
			pl_pk = self.request.GET['pl']
			return get_object_or_404(PerformedLesson, pk=pl_pk)