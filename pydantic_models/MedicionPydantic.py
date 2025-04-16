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

# Clase usada para crear mediciones desde el frontend o Raspberry Pi
class MedicionCreate(MedicionBase):
    pass  # Hereda todos los campos de MedicionBase sin cambios

# Clase para retornar mediciones desde la API con ID generado automáticamente
class Medicion(MedicionBase):
    id: int                               # ID único de la medición (generado automáticamente)

    class Config:
        from_attributes = True            # Permite conversión automática desde objetos SQLAlchemy