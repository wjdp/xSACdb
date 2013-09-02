from models import PerformedSDC
from django import forms

class PerformedSDCCreateForm(forms.ModelForm):
    class Meta:
        model = PerformedSDC
        exclude = ('trainees', 'completed')

class PerformedSDCUpdateForm(forms.ModelForm):
	class Meta:
		model=PerformedSDC
		fields= ('sdc', 'datetime', 'notes')