from datetime import date
from django.forms import ModelForm, DateInput
from django import forms
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from .models import Crop
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': "El correo electrónico no es válido.",
            'required': "El correo electrónico es obligatorio."
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': "El nombre de usuario es obligatorio.",
                'unique': "Este nombre de usuario ya está en uso.",
                'invalid': "El nombre de usuario contiene caracteres no permitidos."
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

class CustomDateInput(forms.DateInput):
    def __init__(self, **kwargs):
        kwargs.setdefault('attrs', {}).update({
            'type': 'date',
            'class': 'form-control',
        })
        super().__init__(**kwargs)

    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        return value.strftime('%Y-%m-%d')

class CreateCropForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['plant'].disabled = True
            self.fields['init_date'].disabled = True

    class Meta:
        model = Crop
        fields = ['name', 'plant', 'init_date', 'last_watering']
        widgets = {
            'init_date': CustomDateInput(),
            'last_watering': CustomDateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        init_date = cleaned_data.get('init_date')
        last_watering = cleaned_data.get('last_watering')

        if name and self.user:
            repeat = Crop.objects.filter(name=name, user=self.user)
            # Para verificar si el nombre ya existe en esta instancia, en update
            if self.instance.pk:
                repeat = repeat.exclude(pk=self.instance.pk)
            if repeat.exists():
                raise forms.ValidationError(
                    "Ya tienes un cultivo con ese nombre.")

        if init_date > date.today():
            raise forms.ValidationError(
                "La fecha de siembra tiene que ser de hoy o anterior a hoy.")

        if last_watering is not None and last_watering > date.today():
            raise forms.ValidationError(
                "La fecha de riego no puede ser superior al día de hoy.")

        if last_watering is not None and last_watering < init_date:
            raise forms.ValidationError(
                "La fecha de riego no puede ser anterior a la de inicio.")

        return cleaned_data
