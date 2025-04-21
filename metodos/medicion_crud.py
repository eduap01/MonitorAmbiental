from sqlalchemy.orm import Session
from models.Medicion import Medicion as MedicionModel
from pydantic_models.MedicionPydantic import MedicionCreate  # Importar desde el directorio schemas
from shapely.geometry import Point
from geoalchemy2.shape import from_shape

# Inserta una nueva medición en la base de datos.
# Recibe datos directamente desde la Raspberry Pi.

def create_medicion(db: Session, medicion: MedicionCreate):
    data = medicion.dict()

    if data["latitud"] is not None and data["longitud"] is not None:
        data["location"] = from_shape(Point(data["longitud"], data["latitud"]), srid=4326)

    db_medicion = MedicionModel(**data)
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion