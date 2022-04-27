import datetime
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from motogram.main.models import Profile, VehiclePhoto, Vehicle
from motogram.main.views.helpers import BootstrapFormMixin, DisabledFieldsFormMixin


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),

            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),

        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),

            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                }
            ),

            'gender': forms.Select(
                choices=Profile.GENDERS,

            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'min': '1900-01-01',
                }
            )

        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        vehicles = list(self.instance.vehicle_set.all())
        VehiclePhoto.objects.filter(tagged_vehicles__in=vehicles).delete()
        self.instance.delete()

        return self.instance

    class Meta:
        model = Profile
        fields = ()


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
