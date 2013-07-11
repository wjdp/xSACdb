from django import forms
from models import MemberProfile

class MemberSearchForm(forms.Form):
    surname=forms.CharField(max_length=50)

class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['dob','home_phone','mobile_phone','address','postcode',
            'veggie','alergies','next_of_kin_name','next_of_kin_relation',
            'next_of_kin_phone']

    def __init__(self, *args, **kwargs):
        super(PersonalEditForm, self).__init__(*args, **kwargs)
        # Make all fields required, then take of the ones that are alright not to
        for field in self.fields:
            self.fields[field].required=True
        self.fields['veggie'].required=False
        self.fields['alergies'].required=False