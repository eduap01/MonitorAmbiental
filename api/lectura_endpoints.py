# api/lectura_endpoints.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from metodos.sensor_crud import insertar_sensor
from metodos.medicion_crud import insertar_medicion
from metodos.registro_sensor_crud import insertar_registro_sensor
from sensors.dht22 import DHT22
from sensors.bmp180 import BMP180
from sensors.mq135 import MQ135
from database import get_db

router = APIRouter()

@router.post("/simular", status_code=200)
def simular_lecturas(db: Session = Depends(get_db)):
    sensor_dht22 = DHT22()
    sensor_bmp180 = BMP180()
    sensor_mq135 = MQ135()

    temperatura = sensor_dht22.leer_temperatura()
    humedad = sensor_dht22.leer_humedad()
    presion = sensor_bmp180.leer_presion()
    calidad_aire = sensor_mq135.leer_calidad_aire()

    # Insertar sensores si no existen
    sensor_dht22 = insertar_sensor(db, "DHT22")
    sensor_bmp180 = insertar_sensor(db, "BMP180")
    sensor_mq135 = insertar_sensor(db, "MQ135")

    # Insertar mediciones
    medicion_dht22 = insertar_medicion(db, temperatura=temperatura, humedad=humedad)
    medicion_bmp180 = insertar_medicion(db, presion=presion)
    medicion_mq135 = insertar_medicion(db, calidad_aire=calidad_aire)

    # Insertar registros de sensores
    insertar_registro_sensor(db, sensor_id=sensor_dht22.id, medicion_id=medicion_dht22.id, tipo_medicion="temperatura", valor=temperatura)
    insertar_registro_sensor(db, sensor_id=sensor_dht22.id, medicion_id=medicion_dht22.id, tipo_medicion="humedad", valor=humedad)
    insertar_registro_sensor(db, sensor_id=sensor_bmp180.id, medicion_id=medicion_bmp180.id, tipo_medicion="presion", valor=presion)
    insertar_registro_sensor(db, sensor_id=sensor_mq135.id, medicion_id=medicion_mq135.id, tipo_medicion="calidad_aire", valor=calidad_aire)

    return {"message": "Lecturas simuladas y almacenadas con éxito"}
