# pydantic_models/RegistroSensorPydantic.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from pydantic import validator
from datetime import datetime

class RegistroSensorCreate(BaseModel):
    sensor_id: int  # Cambiado a int
    medicion_id: int
    tipo_medicion: str
    valor: float
    fecha_registro: datetime

    @validator('fecha_registro')
    def validate_fecha_registro(cls, v):
        # Aquí puedes validar y modificar la fecha si es necesario
        if not isinstance(v, datetime):
            raise ValueError('La fecha debe ser un datetime válido')
        return v

    class Config:
        from_attributes = True


class RegistroSensor(BaseModel):
    id: int
    sensor_id: int
    valor: float
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Para convertir de SQLAlchemy a Pydantic
