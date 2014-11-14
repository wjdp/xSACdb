from django.shortcuts import get_object_or_404
from xsd_members.models import MemberProfile

# Reusable block for the action of pressing the X next to a trainee in the table
# Needs including in the views get method.
def remove_trainee(request, m_inst):
	if 'remove-trainee' in request.GET:
            u=get_object_or_404(MemberProfile, pk=request.GET['remove-trainee'])
            m_inst.trainees.remove(u)
