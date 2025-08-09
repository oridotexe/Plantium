from django.db import migrations
from django.conf import settings
import json
import os

def load_data(apps, schema_editor):
    Plant = apps.get_model('plantium', 'Plant')
    fixture_file = os.path.join(settings.BASE_DIR, 'plantium', 'fixtures', 'plants_data.json')

    base_fields = ['pk']
    
    update_fields = [
        'name', 'variety', 'humidity_min', 'humidity_max', 'temp_min', 'temp_max',
        'img_url', 'watering_freq', 'harvest_duration', 'description'
    ]
    
    with open(fixture_file, encoding='utf-8') as f:
        plants_data = json.load(f)

    for plant_data in plants_data:
        fields = plant_data['fields']
        
        # Preparamos los datos para update_or_create
        base_data = {k: plant_data[k] for k in base_fields}
        defaults = {k: fields[k] for k in update_fields}
        
        Plant.objects.update_or_create(
            **base_data,
            defaults=defaults
        )

class Migration(migrations.Migration):
    dependencies = [
        ('plantium', '0001_initial')
    ]
    operations = [
        migrations.RunPython(load_data)
    ]