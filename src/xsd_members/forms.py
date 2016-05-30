from django import forms
from django.forms.formsets import formset_factory

from models import MemberProfile


class MemberSearchForm(forms.Form):
    surname = forms.CharField(max_length=50)


class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['home_phone', 'mobile_phone', 'address', 'postcode',
                  'veggie', 'alergies', 'next_of_kin_name', 'next_of_kin_relation',
                  'next_of_kin_phone', 'email', 'other_qualifications']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'input-block-level'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 11}),
            'alergies': forms.Textarea(attrs={'rows': 4, 'cols': 11}),
            'other_qualifications': forms.Textarea(
                attrs={'placeholder': 'PADI, CMAS, SSI e.t.c.', 'rows': 4, 'cols': 22}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonalEditForm, self).__init__(*args, **kwargs)
        # Make all REQUIRED_FIELDS required
        for field in MemberProfile.REQUIRED_FIELDS:
            if field in self.fields:
                self.fields[field].required = True


class WelcomeScreenForm(PersonalEditForm):
    class Meta:
        model = MemberProfile
        fields = ['date_of_birth', 'home_phone', 'mobile_phone', 'address', 'postcode',
                  'veggie', 'alergies', 'next_of_kin_name', 'next_of_kin_relation',
                  'next_of_kin_phone']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'input-block-level'}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 11}),
            'alergies': forms.Textarea(attrs={'rows': 4, 'cols': 11}),
        }


class MemberEditForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['date_of_birth', 'home_phone', 'mobile_phone', 'address', 'postcode',
                  'veggie', 'alergies', 'next_of_kin_name', 'next_of_kin_relation',
                  'next_of_kin_phone', 'training_for', 'instructor_number',
                  'student_id',
                  'club_expiry', 'club_membership_type', 'bsac_id', 'bsac_expiry',
                  'bsac_direct_member', 'bsac_member_via_another_club',
                  'bsac_direct_debit', 'medical_form_expiry', 'other_qualifications',
                  'first_name', 'last_name', 'email', ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'other_qualifications': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'alergies': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class FormExpiryForm(forms.Form):
    member_id = forms.IntegerField()
    member_id.widget = forms.HiddenInput()
    full_name = ''
    club_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    bsac_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    medical_form_expiry = forms.DateField(input_formats=['%d/%m/%Y'], required=False)


FormExpiryFormSet = formset_factory(FormExpiryForm)


class MyUserAccountForm(forms.Form):
    email = forms.EmailField()
    new_password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput, required=False)
    new_password_confirm = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput, required=False)


class UserAccountForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    new_password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput, required=False)
