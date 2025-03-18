# api/sensores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.Sensor import Sensor  # Asumiendo que ya tienes este modelo definido
from pydantic_models.SensorPydantic import SensorCreate, SensorResponse  # Modelos Pydantic para validación y respuesta
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un sensor
@router.post("/sensores/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    db_sensor = Sensor(nombre=sensor.nombre, tipo=sensor.tipo)  # Crear el objeto sensor
    db.add(db_sensor)  # Insertar en la base de datos
    db.commit()  # Guardar cambios
    db.refresh(db_sensor)  # Actualizar el objeto con datos como el ID
    return db_sensor  # Devolver el objeto creado
