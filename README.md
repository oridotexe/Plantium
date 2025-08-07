# Plantium
A smart agricultural crop planning system designed to assist farmers in making better decisions about what to plant, when to plant it, and how to manage their land efficiently. PLANTIUM integrates real-time environmental data from temperature and soil moisture sensors (ESP32), as well as weather forecasts via the OpenWeatherMap API.

## Instalación
1. Clona el repositorio:

```Bash
git clone https://github.com/oridotexe/Plantium.git
```

2. Entra en la carpeta del proyecto:

```Bash
cd Plantium
```

3. Crea tu entorno virtual y activalo:

```Bash
python -m venv venv
```

- En Windows:
```Powershell
.\venv\Scripts\Activate.ps1
```

- En Linux:
```Bash
source venv/bin/activate
```

4. Instala dependencias:
```Bash
pip install -r requirements.txt
```

5. Realiza las migraciones:
```Bash
python manage.py migrate
```

6. Cargar datos de plantas:
```Bash
python manage.py loaddata plants_data.json
```

7. Corre el servidor:
```Bash
python manage.py runserver
```
