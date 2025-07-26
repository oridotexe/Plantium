from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from .models import Crop

class CreateCropForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
            Field('name', css_class='form-control mb-3'),
            Field('plant', css_class='form-control mb-3'),
			Field('init_date', css_class='form-control mb-3 ps-5'),
			Field('last_watering', css_class='form-control mb-3 ps-5'),
        )

	class Meta:
		model = Crop
		fields = ['name', 'plant','init_date', 'last_watering']
		widgets = {
            'init_date': DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecciona la fecha'}),
			'last_watering': DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecciona la fecha'}),
        }