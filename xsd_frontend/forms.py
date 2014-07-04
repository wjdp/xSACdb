from django import forms
from models import UpdateRequest

class LoginForm(forms.Form):
    username=forms.CharField(label='Email Address')
    password=forms.CharField(widget=forms.PasswordInput)

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
    email_address = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)

    def clean_password_again(self):
        form_data = self.cleaned_data
        error_message='Passwords do not match'
        if 'password' in form_data and form_data['password'] != form_data['password_again']:
            self._errors["password_again"] = ['Passwords do not match']
            del form_data['password']
            del form_data['password_again']
            print self._errors
        return form_data
