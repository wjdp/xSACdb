from django import forms

from models import Site

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'type',
            'address',
            'location',
            'phone',
            'email',
            'min_temp',
            'max_temp',
            'facilities',
        ]
        # widgets = {
        # 	'facilities': forms.TextInput(),
        # }
