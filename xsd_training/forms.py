from models import *
from xsd_members.models import MemberProfile
from xsd_training.models import Qualification
from django.contrib.auth.models import User
from django import forms

from xSACdb.form_fields import UserModelChoiceField

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

class PoolSheetOptions(forms.Form):
    session = forms.ModelChoiceField(queryset = Session.objects.filter(completed=False), required=True)

    show_public_notes = forms.BooleanField(initial=True, required=False)
    show_private_notes = forms.BooleanField(initial=True, required=False)
    number_of_notes = forms.IntegerField(min_value=0, initial=3, required=False)

    comments_column = forms.BooleanField(initial=True, required=False)
    signature_column = forms.BooleanField(initial=True, required=False)


class TraineeGroupSelectForm(forms.Form):
    traineegroup=forms.ModelChoiceField(queryset=TraineeGroup.objects.all(), label='Trainee Group')
    only_main_three_modes = forms.BooleanField(initial=False)


class TraineeSelectForm(forms.Form):
    trainee = UserModelChoiceField(queryset = User.objects.all().order_by('last_name'))
    qualification = forms.ModelChoiceField(queryset = Qualification.objects.all().exclude(instructor_qualification=True))

class TraineeLessonCompletionDateForm(forms.ModelForm):
    # Need processing for is not partial, is complete
    lesson_data = None
    already_partial = False
    already_completed = False
    display = True
    class Meta:
        model = PerformedLesson
        fields = ['date', 'partially_completed', 'public_notes', 'private_notes']