from django import forms
from models import MemberProfile

from django.forms.formsets import formset_factory

class MemberSearchForm(forms.Form):
    surname=forms.CharField(max_length=50)

class PersonalEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalEditForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = True
        self.fields['home_phone'].required = True
        self.fields['mobile_phone'].required = True
        self.fields['address'].required = True
        self.fields['postcode'].required = True
        self.fields['next_of_kin_name'].required = True
        self.fields['next_of_kin_relation'].required = True
        self.fields['next_of_kin_phone'].required = True

    class Meta:
        model = MemberProfile
        fields = ['date_of_birth','home_phone','mobile_phone','address','postcode',
            'veggie','alergies','next_of_kin_name','next_of_kin_relation',
            'next_of_kin_phone']

    def __init__(self, *args, **kwargs):
        super(PersonalEditForm, self).__init__(*args, **kwargs)
        # Make all fields required, then take of the ones that are alright not to
        for field in self.fields:
            self.fields[field].required=True
        self.fields['veggie'].required=False
        self.fields['alergies'].required=False

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['date_of_birth','home_phone','mobile_phone','address','postcode',
            'veggie','alergies','next_of_kin_name','next_of_kin_relation',
            'next_of_kin_phone','training_for','instructor_number',
            'student_id','associate_id','associate_expiry', 'club_id',
            'club_expiry','club_membership_type','bsac_id','bsac_expiry',
            'bsac_direct_member','bsac_member_via_another_club',
            'bsac_direct_debit','medical_form_expiry','other_qualifications']
        widgets = {
          'address': forms.Textarea(attrs={'rows':3, 'cols':40}),
          'alergies': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }

class FormExpiryForm(forms.Form):
    user_id=forms.IntegerField()
    user_id.widget=forms.HiddenInput()
    full_name=''
    club_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    bsac_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    medical_form_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)

FormExpiryFormSet = formset_factory(FormExpiryForm)

