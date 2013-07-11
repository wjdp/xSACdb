from django import forms

class MemberSearchForm(forms.Form):
	surname=forms.CharField(max_length=50)