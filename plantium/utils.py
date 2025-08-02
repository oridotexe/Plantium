from datetime import date, timedelta
from .models import *
import requests

def calculate_next_watering(last_watering: date , watering_freq: int):
    date_today = date.today()
    prox_watering_date = last_watering + timedelta(days=watering_freq)
    prox_watering_days = (prox_watering_date - date_today).days

    return prox_watering_days

def request_api(latitude: str, longitude: str):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3'
    }

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = "" # Esta es mi clave personal, hay que cambiarla jashja

    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY,
        'units': 'metric',  # Para temperatura en Celsius
        'lang': 'es'  # Opcional: datos en español
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Lanza error si la respuesta no es 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    

    
