from sqlalchemy.orm import Session
from models.Medicion import Medicion as MedicionModel
from pydantic_models.MedicionPydantic import MedicionCreate  # Importar desde el directorio schemas

def create_medicion(db: Session, medicion: MedicionCreate):
    db_medicion = MedicionModel(**medicion.dict())
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion