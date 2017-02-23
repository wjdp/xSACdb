from django.db import models
from django.forms import forms


class DateOfBirthField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(**kwargs)
        return super(DateOfBirthField, self).formfield(**defaults)
