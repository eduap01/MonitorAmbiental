# Monitor Ambiental

Este es un proyecto de monitoreo ambiental con sensores conectados a una Raspberry Pi, visualización web en tiempo real y predicción básica de temperatura usando inteligencia artificial ligera.

---

## Tecnologías utilizadas

- Backend: Python, FastAPI, SQLAlchemy, PostgreSQL
- Frontend: HTML, CSS (Bootstrap), JavaScript (Chart.js, Leaflet.js)
- Base de datos: PostgreSQL
- IA local: Scikit-learn (modelo entrenado con joblib)
- Hardware: Raspberry Pi + sensores DHT22, BMP180, MQ-135

---

## Estructura del proyecto

```
monitor-ambiental/
├── api/                  # Endpoints FastAPI
├── metodos/             # CRUDs
├── models/              # Modelos SQLAlchemy
├── pydantic_models/     # Modelos Pydantic
├── scripts/             # Scripts para entrenamiento y exportación
├── static/              # Archivos frontend (html, css, js)
├── database.py          # Conexión SQLAlchemy
├── main.py              # Arranque de la aplicación FastAPI
├── .gitignore           # Ignora archivos como modelo entrenado o CSVs
```

---

## Cómo ejecutar el proyecto localmente

1. Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/monitor-ambiental.git
cd monitor-ambiental
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Inicia la base de datos PostgreSQL y crea la base de datos llamada `monitoreo_ambiental`.

5. Ejecuta la aplicación:
```bash
uvicorn main:app --reload
```

6. Abre en tu navegador:
```
http://localhost:8000
```

---

## Scripts disponibles

- `scripts/exportar_datos.py` → exporta mediciones a CSV desde PostgreSQL.
- `scripts/entrenar_modelo.py` → entrena modelo de predicción de temperatura.

> El archivo `modelo_temp_rpi.joblib` se genera desde el script de entrenamiento y no está incluido en el repositorio por defecto.

---

## Archivos ignorados en .gitignore recomendado

```gitignore
*.pyc
__pycache__/
.env
*.joblib
scripts/*.csv
venv/
```

---

## Descripción del sistema

- Panel de control lateral con filtros, comparaciones y selección de variables.
- Gráfica en tiempo real de temperatura, humedad, presión o calidad del aire.
- Predicción de temperatura con IA ligera (TinyIA).
- Mapa con ubicación del sensor y opción de centrar en tu posición actual.
- Modo claro/oscuro para visualización adaptable.

### Sensores utilizados:

- DHT22: mide temperatura y humedad con buena precisión.
- BMP180: sensor barométrico para presión atmosférica.
- MQ-135: sensor de gases para estimar calidad del aire. Puede conectarse a entrada analógica o digital.

Estos sensores se conectan a una Raspberry Pi 3B+ que recolecta los datos, los envía al backend vía API, y pueden ser almacenados y visualizados en tiempo real.

---

## Desarrollo en Raspberry Pi

1. Instalar librerías necesarias en la Raspberry Pi:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install requests Adafruit-BMP PythonDHT joblib
```

2. Organiza tus scripts en la carpeta `monitoring/` (por ejemplo):
```
/home/pi/monitoring/
├── geo_sender.py
├── sensor_reader.py
├── edicion_sender.py
├── modelo_temp_rpi.joblib
```

3. Asegúrate de que la Raspberry Pi tenga conexión de red con la PC que ejecuta el backend (puede ser en red local o usando túneles).

4. Para enviar la ubicación desde la Raspberry Pi al backend expuesto públicamente:

Si el servidor está en localhost, usa [ngrok](https://ngrok.com) para exponer el puerto 8000:
```bash
ngrok http 8000
```
Esto generará una URL pública como `https://abc123.ngrok.io`, que puedes usar en los scripts de la Raspberry Pi para enviar datos.

5. Configura el script `geo_sender.py` para hacer un `POST` a `/api/ubicacion/` con la ubicación deseada.

---

## Author / License

Este proyecto fue creado como parte de un trabajo de desarrollo con Raspberry Pi. Puedes usarlo, adaptarlo y compartirlo con fines educativos.

---

## Project in English

This project monitors environmental data using sensors connected to a Raspberry Pi, with a web interface and basic temperature prediction using a lightweight AI model.

To run it locally:
1. Clone the repo, install requirements, and run with `uvicorn`.
2. Visit `http://localhost:8000` to access the web dashboard.

It includes:
- Real-time sensor visualization
- Environmental predictions using a linear regression model
- Map integration with sensor and user location
- Filtering and comparison of sensor data

Sensor data is read via Raspberry Pi and sent to a FastAPI backend for processing and display.

See `scripts/` for data export and training utilities.

