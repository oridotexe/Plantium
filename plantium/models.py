from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    humidity_min = models.FloatField()
    humidity_max = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    img_url = models.URLField(blank=True, null=True)
    watering_freq = models.IntegerField(help_text="Frecuencia en días")
    harvest_duration = models.IntegerField(help_text="Duración en días")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - ({self.variety})"


class Crop(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Cultivo")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="crops", verbose_name="Planta") # NOQA
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crops") # NOQA
    init_date = models.DateField(verbose_name="Fecha de inicio")
    last_watering = models.DateField(blank=True, null=True, verbose_name="Ultimo riego")
    status = models.IntegerField(default=0)

    class Meta:
        unique_together = ['name', 'user']

    def __str__(self):
        return f"{self.name} de {self.user.username}"
