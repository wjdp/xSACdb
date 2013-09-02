from django import forms
from models import UpdateRequest

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UpdateRequestMake(forms.ModelForm):
    class Meta:
        model=UpdateRequest
        fields=['area', 'lesson', 'site', 'request_body']

class UpdateRequestReply(forms.ModelForm):
    class Meta:
        model=UpdateRequest
        fields=['response_body','completed']