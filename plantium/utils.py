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

def create_data_list(cleaned_data: dict):
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

    return { 'temps': temps, 'hums': hums }

def generate_recomendations(temps, hums):
    recommended_plants = []
    all_plants = Plant.objects.all()
    MARGIN = 1.10

    # Calcular percentiles (ej: 10% y 90% para evitar extremos)
    temp_p10 = np.percentile(temps, 10)  # Temperatura mínima esperada
    temp_p90 = np.percentile(temps, 90)  # Temperatura máxima esperada


    hum_p10 = np.percentile(hums, 10)
    hum_p90 = np.percentile(hums, 90)

    print("\nTemp_p10", temp_p10, "\n")
    print("Temp_p90", temp_p90, "\n")
    print("H10", hum_p10, "\n")
    print("H90", hum_p90, "\n")
    
    for obj_plant in all_plants:
        # 1. Verificar rangos ideales con percentiles
        temp_ok = (MARGIN * obj_plant.temp_min <= temp_p10) and (temp_p90 <= obj_plant.temp_max * MARGIN)
        hum_ok = (MARGIN * obj_plant.humidity_min <= hum_p10) and (hum_p90 <= obj_plant.humidity_max * MARGIN)
        
        # 2. Verificar umbrales críticos
        # no_hielo = temp_min >= obj_plant.temp_critica_min
        # no_ola_calor = temp_max <= obj_plant.temp_critica_max
        
        # 3. Validar estabilidad climática (solo para obj_plants sensibles)
        # estable = (temp_std <= 3.0) if obj_plant.sensible else True
        
        # if temp_ok and hum_ok: # and no_hielo and no_ola_calor and estable
        #     recommended_plants.append(obj_plant)

        if (temp_p10 >= obj_plant.temp_min) and (temp_p90 <= obj_plant.temp_max):
            temp_score = 100
        elif (temp_p10 >= obj_plant.temp_min * MARGIN) and (temp_p90 <= obj_plant.temp_max * MARGIN):
            temp_score = 50
        else:
            temp_score = 0

        # 2. Puntuar humedad (0-100)
        if (hum_p10 >= obj_plant.humidity_max) and (hum_p90 <= obj_plant.humidity_max):
            hum_score = 100
        elif (hum_p10 >= obj_plant.humidity_max * MARGIN) and (hum_p90 <= obj_plant.humidity_max * MARGIN):  # Tolerancia del 15%
            hum_score = 50
        else:
            hum_score = 0

        # 3. Ajustar por lluvia próxima
        # rain_boost = 20 if rain_next_24h > 10 else 0  # Bonus si llueve >10mm

        # Puntaje total (ponderado)
        total_score = 0.8 * temp_score + 0.2 * hum_score # + 0.1  * rain_boost
        print("TOTAL SCORE: ", total_score)
        if total_score >= 60:
            recommended_plants.append(obj_plant)
    
    return recommended_plants
