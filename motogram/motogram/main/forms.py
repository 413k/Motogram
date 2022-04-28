from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from motogram.main.models import Vehicle
from motogram.common.helpers import BootstrapFormMixin, DisabledFieldsFormMixin



class CreateVehicleForm(BootstrapFormMixin, forms.ModelForm):
    MIN_YEAR_OF_CREATION = date(1900, 1, 1)
    MAX_YEAR_OF_CREATION = date.today()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        vehicle = super().save(commit=False)

        vehicle.user = self.user
        if commit:
            vehicle.save()

        return vehicle

    def clean_year_of_creation(self):
        year_of_creation = self.cleaned_data['year_of_creation']
        if year_of_creation < self.MIN_YEAR_OF_CREATION or self.MAX_YEAR_OF_CREATION < year_of_creation:
            raise ValidationError(
                f'Year of creation must be between {self.MIN_YEAR_OF_CREATION} and {self.MAX_YEAR_OF_CREATION}')

        return year_of_creation

    class Meta:
        model = Vehicle
        exclude = ('user',)
        widgets = {
            'brand': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your vehicle brand',
                }
            ),
        }


class EditVehicleForm(BootstrapFormMixin, forms.ModelForm):
    MIN_YEAR_OF_CREATION = date(1900, 1, 1)
    MAX_YEAR_OF_CREATION = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean_year_of_creation(self):
        year_of_creation = self.cleaned_data['year_of_creation']
        if year_of_creation < self.MIN_YEAR_OF_CREATION or self.MAX_YEAR_OF_CREATION < year_of_creation:
            raise ValidationError(
                f'Year of creation must be between {self.MIN_YEAR_OF_CREATION} and {self.MAX_YEAR_OF_CREATION}')

        return year_of_creation

    class Meta:
        model = Vehicle
        exclude = ('user_profile',)


class DeleteVehicleForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Vehicle
        exclude = ('user_profile',)
