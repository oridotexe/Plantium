from celery import shared_task
from django.core import management

@shared_task
def run_check_watering():
    management.call_command("check_watering")
