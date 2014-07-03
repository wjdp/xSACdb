from models import *
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

class SessionCreateForm(forms.ModelForm):
	class Meta:
		model=Session
		fields=['when','where','notes','created_by']

class SessionPLMapForm(forms.ModelForm):	# Used for mapping trainees to lessons and instructors in a Session
    def __init__(self,*args,**kwargs):
    	super(SessionPLMapForm, self).__init__(*args,**kwargs)

        # Exclude experience dives from the selection
    	self.fields['lesson'].queryset=Lesson.objects.exclude(mode='XP').order_by('qualification','mode')

    class Meta:
        model = PerformedLesson
        fields=['lesson', 'instructor']

class SessionCompleteForm(forms.ModelForm):
    class Meta:
        model = PerformedLesson
        fields = ['completed', 'partially_completed', 'public_notes', 'private_notes']
    

class TraineeGroupSelectForm(forms.Form):
    traineegroup=forms.ModelChoiceField(queryset=TraineeGroup.objects.all(), label='Trainee Group')