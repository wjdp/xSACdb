from django import forms
from django.core.exceptions import ValidationError


class DynForm(forms.Form):
    """
    Dynamic form that allows the user to change and then verify the data that was parsed
    """

    def setFields(self, kwds):
        """
        Set the fields in the form
        """
        keys = kwds.keys()
        keys.sort()
        for k in keys:
            self.fields[k] = kwds[k]

    def setData(self, kwds):
        """
        Set the data to include in the form
        """
        keys = kwds.keys()
        keys.sort()
        for k in keys:
            self.data[k] = kwds[k]

    def validate(self, post):
        """
        Validate the contents of the form
        """
        self.cleaned_data = {}
        for name, field in self.fields.items():
            try:
                self.cleaned_data[name] = field.clean(post[name])
            except ValidationError as e:
                self.errors[name] = e.messages
