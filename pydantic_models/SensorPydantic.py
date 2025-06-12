# pydantic_models/SensorPydantic.py
from pydantic import BaseModel
from uuid import UUID

#Parte descartada del proyecto. Ahora no tiene funcionalidad

class SensorCreate(BaseModel):
    nombre: str
    tipo: str

class SensorResponse(BaseModel):
    id: int
    nombre: str
    tipo: str

    class Config:
        from_attributes = True  # Permite convertir automáticamente de SQLAlchemy
