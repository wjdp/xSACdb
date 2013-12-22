from models import PerformedSDC, Qualification
from xsd_members.models import MemberProfile
from django import forms

class PerformedSDCCreateForm(forms.ModelForm):
    class Meta:
        model = PerformedSDC
        exclude = ('trainees', 'completed')

class PerformedSDCUpdateForm(forms.ModelForm):
	class Meta:
		model=PerformedSDC
		fields= ('sdc', 'datetime', 'notes')

class QualificationSelectForm(forms.Form):
	qualification=forms.ModelChoiceField(queryset=Qualification.objects.all())
	selected_members=forms.ModelMultipleChoiceField(
		queryset=MemberProfile.objects.all())
