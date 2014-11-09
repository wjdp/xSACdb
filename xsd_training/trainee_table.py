from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Reusable block for the action of pressing the X next to a trainee in the table
# Needs including in the views get method.
def remove_trainee(request, m_inst):
	if 'remove-trainee' in request.GET:
            u=get_object_or_404(get_user_model(), pk=request.GET['remove-trainee'])
            m_inst.trainees.remove(u)
