from __future__ import unicode_literals

from allauth.account.forms import SignupForm
from django import forms

from models import UpdateRequest


class UpdateRequestMake(forms.ModelForm):
    class Meta:
        model = UpdateRequest
        fields = ['area', 'lesson', 'site', 'request_body']


class UpdateRequestReply(forms.ModelForm):
    class Meta:
        model = UpdateRequest
        fields = ['response_body', 'completed']


class ClassicSignupForm(SignupForm):
    first_name = forms.CharField(label='Forename', widget=forms.TextInput(attrs={'placeholder': 'Forename'}))
    last_name = forms.CharField(label='Surname', widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
