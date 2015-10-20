from django import forms

from allauth.socialaccount.forms import SignupForm as SocialSignupForm

class SignupForm(SocialSignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
