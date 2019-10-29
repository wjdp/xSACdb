

from django import forms
from django.core.exceptions import ValidationError

from xsd_trips.models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            'name',
            'date_start',
            'date_end',
            'cost',
            'spaces',
            'max_depth',
            'min_qual',
            'description',
        )

    def clean_date_end(self):
        cleaned_data = super(TripForm, self).clean()
        start_date = cleaned_data.get('date_start')
        end_date = cleaned_data.get('date_end')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date should be greater than start date.')
        return end_date
