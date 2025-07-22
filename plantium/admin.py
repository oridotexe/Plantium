from django.contrib import admin

# Register your models here.
from .models import Plant, Crop

admin.site.register(Plant)
admin.site.register(Crop)