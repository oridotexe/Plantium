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
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateCropForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

	class Meta:
		model = Crop
		fields = ['name', 'plant','init_date', 'last_watering']
		widgets = {
        	'init_date': DateInput(
				attrs={'type': 'date', 'class': 'form-control'}
			),
			'last_watering': DateInput(
				attrs={'type': 'date', 'class': 'form-control'}
			),
        }

	def clean(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name')
		init_date = cleaned_data.get('init_date')
		last_watering = cleaned_data.get('last_watering')

		if name and self.user:
			exists = Crop.objects.filter(name=name, user=self.user).exists()
			if exists:
				raise forms.ValidationError("Ya tienes un cultivo con ese nombre.")
			
		if init_date > date.today():
			raise forms.ValidationError("La fecha de siembra tiene que ser de hoy o anterior a hoy.")
			
		if last_watering is not None and last_watering < init_date:
			raise forms.ValidationError("La fecha de riego no puede ser anterior a la de inicio.")
		
		return cleaned_data