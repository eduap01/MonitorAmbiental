# api/registro_sensores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import pydantic_models
from metodos.registro_sensor_crud import create_registro_sensor  # Lógica de inserción
from models.Sensor import Sensor

from pydantic_models.RegistroSensorPydantic import RegistroSensorCreate, RegistroSensor  # Modelos Pydantic para validación y respuesta
from database import SessionLocal
from uuid import UUID

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un registro de sensor
@router.post("/registros_sensores/")
def create_registro_sensor_endpoint(
    registro: pydantic_models.RegistroSensorPydantic.RegistroSensorCreate, db: Session = Depends(get_db)
):
    return create_registro_sensor(db=db, registro=registro)