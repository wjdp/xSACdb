from django import forms
from django.contrib.auth.forms import AuthenticationForm

from models import UpdateRequest
from xsd_auth.models import User


class LoginForm(AuthenticationForm):
    username=forms.CharField(max_length=254, label='Email')
    # password=forms.CharField(widget=forms.PasswordInput)

class UpdateRequestMake(forms.ModelForm):
    class Meta:
        model=UpdateRequest
        fields=['area', 'lesson', 'site', 'request_body']

class UpdateRequestReply(forms.ModelForm):
    class Meta:
        model=UpdateRequest
        fields=['response_body','completed']

class UserRegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email_address(self):
        form_data = self.cleaned_data
        if 'email' in form_data and User.objects.filter(email=form_data['email']):
            self.add_error('email_address', 'An account on this site is already using that email address')
        return form_data['email']

    def clean_password(self):
        form_data = self.cleaned_data
        if 'password' in form_data and len(form_data['password']) < 8:
            self.add_error('password', 'Password must be at least 8 characters')
        return form_data['password']

