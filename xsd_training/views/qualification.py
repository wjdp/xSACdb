from django.shortcuts import render
from django.template import RequestContext

from xSACdb.roles.decorators import require_training_officer
from xSACdb.roles.mixins import RequireTrainingOfficer

from xsd_training.models import *
from xsd_training.forms import *
import xsd_training.trainee_table as trainee_table


from xsd_members.bulk_select import get_bulk_members


@require_training_officer
def QualificationAward(request):
    qual_form=None
    selected_members=None

    if 'names' in request.GET and request.GET['names']!='':
        selected_members=get_bulk_members(request)
        qual_form=QualificationSelectForm(initial={'selected_members':selected_members})

    if request.POST:
        qual_form=QualificationSelectForm(request.POST)
        if qual_form.is_valid():
            for member in qual_form.cleaned_data['selected_members']:
                member.qualifications.add(qual_form.cleaned_data['qualification'])
                member.save()
            return render(request, 'qualification_award.html', {
                'completed': True,
                'selected_members': qual_form.cleaned_data['selected_members'],
                'qualification': qual_form.cleaned_data['qualification'],
            }, context_instance=RequestContext(request))

    return render(request, 'qualification_award.html', {
        'qual_form': qual_form,
        'selected_members': selected_members,
        'completed': False
    }, context_instance=RequestContext(request))
