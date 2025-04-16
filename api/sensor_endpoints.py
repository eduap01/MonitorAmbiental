
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from metodos.sensor_crud import create_sensor
from models.Sensor import Sensor
from pydantic_models.SensorPydantic import SensorCreate, SensorResponse  # Modelos Pydantic para validación y respuesta
from database import SessionLocal

# Endpoint para insertar un sensor nuevo en la BD.
# Usado para inicializar el sistema o añadir nuevos sensores posteriormente.

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un sensor
@router.post("/sensores/", response_model=SensorResponse)
def create_sensor_endpoint(sensor: SensorCreate, db: Session = Depends(get_db)):
    db_sensor = create_sensor(db=db, nombre=sensor.nombre, tipo=sensor.tipo)
    return db_sensor
