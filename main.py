from fastapi import FastAPI
from pydantic import BaseModel
from models.lectura import guardar_lectura
from sensors.dht22 import DHT22
from sensors.bmp180 import BMP80
from sensors.mq135 import MQ135

# Instanciar los sensores
sensor_dht22 = DHT22()
sensor_bmp180 = BMP80()
sensor_mq135 = MQ135()

# Inicializar FastAPI
app = FastAPI()

# Modelo de entrada para las lecturas de sensores
class LecturaSensor(BaseModel):
    sensor_id: int
    tipo: str
    valor: float

@app.get("/")
def read_root():
    return {"message": "Sistema de Monitoreo Ambiental"}

@app.post("/lectura/")
def insertar_lectura(lectura: LecturaSensor):
    # Guardar la lectura en la base de datos
    guardar_lectura(lectura.sensor_id, lectura.tipo, lectura.valor)
    return {"message": f"Lectura de {lectura.tipo} guardada con éxito"}

# Ruta para obtener las lecturas simuladas (solo como ejemplo)
@app.get("/simulacion/")
def simulacion():
    # Simulación de lecturas
    temperatura = sensor_dht22.leer_temperatura()
    humedad = sensor_dht22.leer_humedad()
    presion = sensor_bmp180.leer_presion()
    calidad_aire = sensor_mq135.leer_calidad_aire()

    # Mostrar las lecturas (en la consola o log)
    print(f"Temperatura: {temperatura}°C")
    print(f"Humedad: {humedad}%")
    print(f"Presión: {presion} hPa")
    print(f"Calidad del aire: {calidad_aire} ppm")

    # Guardar las lecturas en la base de datos
    guardar_lectura(1, "temperatura", temperatura)  # DHT22
    guardar_lectura(1, "humedad", humedad)          # DHT22
    guardar_lectura(2, "presion", presion)          # BMP180
    guardar_lectura(3, "calidad_aire", calidad_aire) # MQ135

    return {"message": "Simulaciones de sensores guardadas"}
