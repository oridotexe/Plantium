from datetime import date, timedelta
from .models import *

def calculate_next_watering(last_watering: date , watering_freq: int):
    date_today = date.today()
    prox_watering_date = last_watering + timedelta(days=watering_freq)
    prox_watering_days = (prox_watering_date - date_today).days

    return prox_watering_days
