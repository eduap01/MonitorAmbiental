from models.lectura import guardar_lectura
from sensors.dht22 import DHT22
from sensors.bmp180 import BMP180
from sensors.mq135 import MQ135
from sqlalchemy.orm import Session

# Inicialización de sensores
sensor_dht22 = DHT22()
sensor_bmp180 = BMP180()
sensor_mq135 = MQ135()

def simular_lecturas(db: Session):
    """
    Simula las lecturas de los sensores y las guarda en la base de datos.
    """
    try:
        # Simulación de lecturas
        temperatura = sensor_dht22.leer_temperatura()
        humedad = sensor_dht22.leer_humedad()
        presion = sensor_bmp180.leer_presion()
        calidad_aire = sensor_mq135.leer_calidad_aire()

        # Mostrar las lecturas en la consola (o log)
        print(f"Temperatura: {temperatura}°C")
        print(f"Humedad: {humedad}%")
        print(f"Presión: {presion} hPa")
        print(f"Calidad del aire: {calidad_aire} ppm")

        # Guardar las lecturas en la base de datos
        guardar_lectura(sensor_id=1, temperatura=temperatura, humedad=humedad, db=db)  # DHT22
        guardar_lectura(sensor_id=2, presion=presion, db=db)  # BMP180
        guardar_lectura(sensor_id=3, calidad_aire=calidad_aire, db=db)  # MQ135

    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
        raise  # Relanza la excepción para que pueda ser manejada en `main.py`