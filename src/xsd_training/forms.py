from __future__ import unicode_literals

from django import forms
# from xSACdb.widgets import AdminDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from models import *
from xSACdb.form_fields import UserModelChoiceField
from xsd_members.models import MemberProfile
from xsd_training.models import Qualification, SDC


class PerformedSDCCreateForm(forms.ModelForm):
    class Meta:
        model = PerformedSDC
        exclude = ('trainees', 'completed')


class PerformedSDCUpdateForm(forms.ModelForm):
    class Meta:
        model = PerformedSDC
        fields = ('datetime', 'notes')


class QualificationSelectForm(forms.Form):
    qualification = forms.ModelChoiceField(queryset=Qualification.objects.all())
    selected_members = forms.ModelMultipleChoiceField(
        queryset=MemberProfile.objects.all())


class SDCSelectForm(forms.Form):
    sdc = forms.ModelChoiceField(queryset=SDC.objects.all())
    selected_members = forms.ModelMultipleChoiceField(
        queryset=MemberProfile.objects.all())


class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'when', 'where', 'notes']
        widgets = {
            'when': AdminDateWidget(),
        }


class SessionPLMapForm(forms.ModelForm):  # Used for mapping trainees to lessons and instructors in a Session
    def __init__(self, *args, **kwargs):
        super(SessionPLMapForm, self).__init__(*args, **kwargs)

        # Exclude experience dives from the selection
        self.fields['lesson'].queryset = Lesson.objects.exclude(mode='XP').order_by('qualification', 'mode')
        # self.fields['instructor'].queryset=MemberProfile.objects.all()

    class Meta:
        model = PerformedLesson
        fields = ['lesson', 'instructor']


class SessionCompleteForm(forms.ModelForm):
    class Meta:
        model = PerformedLesson
        fields = ['completed', 'partially_completed', 'public_notes', 'private_notes']


class PoolSheetOptions(forms.Form):
    # DB order_by on left, friendly UI option right
    POOLSHEET_SORT_BY = (
        ('instructor__last_name', 'Instructor'),
        ('trainee__last_name', 'Trainee'),
        ('lesson__order', 'Lesson'),
    )

    session = forms.ModelChoiceField(queryset=Session.objects.filter(completed=False), required=True)

    sort_by = forms.ChoiceField(choices=POOLSHEET_SORT_BY)

    show_public_notes = forms.BooleanField(initial=True, required=False)
    show_private_notes = forms.BooleanField(initial=True, required=False)
    number_of_notes = forms.IntegerField(min_value=0, initial=3, required=False)

    comments_column = forms.BooleanField(initial=True, required=False)
    signature_column = forms.BooleanField(initial=True, required=False)


class TraineeGroupSelectForm(forms.Form):
    traineegroup = forms.ModelChoiceField(queryset=TraineeGroup.objects.all(), label='Trainee Group')
    # only_main_three_modes = forms.BooleanField(initial=False)


class TraineeSelectForm(forms.Form):
    trainee = UserModelChoiceField(queryset=MemberProfile.objects.all().order_by('last_name'))
    qualification = forms.ModelChoiceField(queryset=Qualification.objects.all().exclude(instructor_qualification=True))


class TraineeLessonCompletionDateForm(forms.ModelForm):
    # Need processing for is not partial, is complete
    lesson_data = None
    already_partial = False
    already_completed = False
    display = True

    class Meta:
        model = PerformedLesson
        fields = ['date', 'partially_completed', 'public_notes', 'private_notes']


class MiniQualificationForm(forms.Form):
    def __init__(self, trainee=None, *args, **kwargs):
        super(MiniQualificationForm, self).__init__(*args, **kwargs)
        self.fields['qualification'] = forms.ModelChoiceField(
            queryset=Qualification.objects.get_active(trainee).filter(instructor_qualification=False),
            empty_label="X Remove")

    # qualification = forms.ModelChoiceField(
    #     queryset=Qualification.objects.filter(instructor_qualification=False), empty_label="X Remove")


class MiniQualificationSetForm(MiniQualificationForm):
    field = forms.CharField(widget=forms.HiddenInput(), initial='current_qual')


class MiniTrainingForSetForm(MiniQualificationForm):
    field = forms.CharField(widget=forms.HiddenInput(), initial='training_for')


class MiniInstructorQualificationSetForm(MiniQualificationForm):
    qualification = forms.ModelChoiceField(
        queryset=Qualification.objects.filter(instructor_qualification=True), empty_label="X Remove")
    number = forms.IntegerField()
    field = forms.CharField(widget=forms.HiddenInput(), initial='instructor_qual')


class MiniTraineeSDCAddForm(forms.Form):
    sdc = forms.ModelChoiceField(queryset=SDC.objects.all())
    field = forms.CharField(widget=forms.HiddenInput(), initial='sdc')


class PerformedQualificationForm(forms.ModelForm):
    class Meta:
        model = PerformedQualification
        exclude = []

    def clean(self):
        cleaned_data = super(PerformedQualificationForm, self).clean()
        mode = cleaned_data.get('mode')
        xo_from = cleaned_data.get('xo_from')

        # Put a arbitrary minimum character limit here of 4, could probably make higher but let's play safe
        if mode == 'XO' and len(xo_from) <= 4:
            self.add_error('xo_from', 'This field is required when the mode is crossover.')
