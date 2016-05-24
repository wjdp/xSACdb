from django import forms
from django.forms.formsets import formset_factory

from models import MemberProfile
from xSACdb.forms import DynForm


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
        # Make all fields required, then take of the ones that are alright not to
        for field in self.fields:
            self.fields[field].required = True
        self.fields['veggie'].required = False
        self.fields['alergies'].required = False


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


class DynamicUpdateProfileForm(DynForm):
    def setUp(self, member_profile):
        self.member_profile = member_profile
        # Work out what fields we need given a MemberProfile and set them up
        form_fields = {}
        for REQUIRED_FIELD in member_profile.REQUIRED_FIELDS:
            model_field = member_profile._meta.get_field(REQUIRED_FIELD)
            form_fields[REQUIRED_FIELD] = model_field.formfield()
            form_fields[REQUIRED_FIELD].required = True
        for OPTIONAL_FIELD in member_profile.OPTIONAL_FIELDS:
            model_field = member_profile._meta.get_field(OPTIONAL_FIELD)
            form_fields[OPTIONAL_FIELD] = model_field.formfield()
        self.setFields(form_fields)

    def save(self):
        for key, value in self.cleaned_data.iteritems():
            setattr(self.member_profile, key, value)
        self.member_profile.save()



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
