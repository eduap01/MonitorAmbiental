from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicionBase(BaseModel):
    fecha_hora: datetime
    temperatura: float
    humedad: float
    calidad_aire: float
    presion: float
    prediccion: Optional[float] = None

class MedicionCreate(MedicionBase):
    pass

class Medicion(MedicionBase):
    id: int

    class Config:
        from_attributes  = True