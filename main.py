from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models.lectura import guardar_lectura, LecturaSensor
from sensors.dht22 import DHT22
from sensors.bmp180 import BMP180
from sensors.mq135 import MQ135
from simulacion import simular_lecturas

# Inicialización de sensores
sensor_dht22 = DHT22()
sensor_bmp180 = BMP180()
sensor_mq135 = MQ135()

# Crear la aplicación FastAPI
app = FastAPI()

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Modelo Pydantic para validar los datos de entrada
class LecturaSensorModel(BaseModel):
    sensor_id: int
    temperatura: float | None = None
    humedad: float | None = None
    calidad_aire: float | None = None
    presion: float | None = None


@app.get("/")
def read_root():
    return {"message": "Sistema de Monitoreo Ambiental"}

@app.post("/lectura/")
def insertar_lectura(lectura: LecturaSensorModel, db: Session = Depends(get_db)):
    try:
        guardar_lectura(
            sensor_id=lectura.sensor_id,
            temperatura=lectura.temperatura,
            humedad=lectura.humedad,
            calidad_aire=lectura.calidad_aire,
            presion=lectura.presion,
            db=db
        )
        return {"message": "Lectura guardada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la lectura: {str(e)}")

@app.get("/lecturas/")
def obtener_todas_lecturas(db: Session = Depends(get_db)):
    try:
        # Consultar todas las lecturas en la base de datos
        lecturas = db.query(LecturaSensor).all()
        return lecturas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las lecturas: {str(e)}")

# Ruta para simular lecturas de sensores
@app.get("/simulacion/")
def simulacion(db: Session = Depends(get_db)):
    try:
        # Llamar a la función de simulación
        simular_lecturas(db)
        return {"message": "Simulaciones de sensores guardadas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la simulación: {str(e)}")


@app.get("/lecturas/recientes/")
def obtener_lecturas_recientes(db: Session = Depends(get_db)):
    try:
        # Obtener la lectura más reciente de cada parámetro
        lectura_temperatura = (
            db.query(LecturaSensor)
            .filter(LecturaSensor.temperatura.isnot(None))  # Filtrar lecturas con temperatura
            .order_by(desc(LecturaSensor.fecha_hora))  # Ordenar por fecha_hora descendente
            .first()
        )

        lectura_humedad = (
            db.query(LecturaSensor)
            .filter(LecturaSensor.humedad.isnot(None))  # Filtrar lecturas con humedad
            .order_by(desc(LecturaSensor.fecha_hora))
            .first()
        )

        lectura_calidad_aire = (
            db.query(LecturaSensor)
            .filter(LecturaSensor.calidad_aire.isnot(None))  # Filtrar lecturas con calidad_aire
            .order_by(desc(LecturaSensor.fecha_hora))
            .first()
        )

        lectura_presion = (
            db.query(LecturaSensor)
            .filter(LecturaSensor.presion.isnot(None))  # Filtrar lecturas con presión
            .order_by(desc(LecturaSensor.fecha_hora))
            .first()
        )

        # Crear un diccionario con las lecturas más recientes
        lecturas_recientes = {
            "temperatura": lectura_temperatura,
            "humedad": lectura_humedad,
            "calidad_aire": lectura_calidad_aire,
            "presion": lectura_presion,
        }

        return lecturas_recientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las lecturas recientes: {str(e)}")
