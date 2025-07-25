from django.forms import ModelForm
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
			Field('init_date', css_class='form-control mb-3'),
        )

	class Meta:
		model = Crop
		fields = ['name', 'plant','init_date']