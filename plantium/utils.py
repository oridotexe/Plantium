from django.conf import settings
from .models import *
from datetime import date, timedelta
import requests
import numpy as np

def calculate_next_watering(last_watering: date , watering_freq: int):
    date_today = date.today()
    prox_watering_date = last_watering + timedelta(days=watering_freq)
    prox_watering_days = (prox_watering_date - date_today).days

    return prox_watering_days

def request_api(latitude: str, longitude: str, is_current: bool):
    extension = "weather" if is_current else "forecast"

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3'
    }

    base_url = "https://api.openweathermap.org/data/2.5/" + extension

    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': settings.OPENWEATHER_API_KEY,
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
    
def process_weather_data(data: dict):
    cleaned_data = {}
    if 'list' not in data:
        cleaned_data = {
            'temp': data.get('main', {}).get('temp', 'N/A'),  # 'N/A' si no existe
            'hum': data.get('main', {}).get('humidity', 'N/A'),
            'description': data.get('weather', [{}])[0].get('description', 'N/A')
        }
    else:
        list_data = data.get('list', [])
        if not isinstance(list_data, list):  # Por si 'list' no es una lista
            return {"error": "Formato de pronóstico no válido"}
        
        cleaned_data = {
            i: {
                'date': item.get('dt_txt', 'Fecha no disponible'),
                'temp': item.get('main', {}).get('temp', 'N/A'),
                'hum': item.get('main', {}).get('humidity', 'N/A')
            }
            for i, item in enumerate(list_data)
        }

    return cleaned_data

def average_weather(cleaned_data: dict):
    temps = [
        i['temp'] 
        for i in cleaned_data.values() 
        if isinstance(i.get('temp'), (int, float))  # Solo números
    ]
    
    hums = [
        i['hum'] 
        for i in cleaned_data.values() 
        if isinstance(i.get('hum'), (int, float))
    ]

    avg_temp = sum(temps) / len(temps) if temps else None
    avg_hum = sum(hums) / len(hums) if hums else None

    return { 'avg_temp': avg_temp, 'avg_hum': avg_hum }
