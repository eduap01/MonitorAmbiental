from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.orm import Session
from database import Base, get_db
from models.sensor import Sensor


class LecturaSensor(Base):
    __tablename__ = 'lecturas_sensores'

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, nullable=False)
    temperatura = Column(Numeric(5, 2), nullable=True)
    humedad = Column(Numeric(5, 2), nullable=True)
    calidad_aire = Column(Numeric(5, 2), nullable=True)
    presion = Column(Numeric(7, 2), nullable=True)
    fecha_hora = Column(DateTime, nullable=True)

def guardar_lectura(sensor_id: int, temperatura: float = None, humedad: float = None, calidad_aire: float = None, presion: float = None, db: Session = None):
    """
    Guarda una lectura en la base de datos.
    """
    if db is None:
        raise ValueError("La sesión de la base de datos (db) no puede ser nula.")

    try:
        # Verificar si el sensor_id existe en la tabla sensores
        sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
        if not sensor:
            print(f"Error: El sensor_id={sensor_id} no existe en la tabla sensores.")
            return

        # Crear una nueva lectura
        nueva_lectura = LecturaSensor(
            sensor_id=sensor_id,
            temperatura=temperatura,
            humedad=humedad,
            calidad_aire=calidad_aire,
            presion=presion,
            fecha_hora=datetime.now()
        )

        # Añadir y guardar la lectura
        db.add(nueva_lectura)
        db.commit()
        db.refresh(nueva_lectura)

        print(f"✅ Lectura guardada: Sensor {sensor_id} | Temp: {temperatura}°C | Hum: {humedad}% | Calidad: {calidad_aire} | Presión: {presion} hPa")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar en la base de datos: {e}")
        raise  # Relanza la excepción para que pueda ser manejada en el llamador