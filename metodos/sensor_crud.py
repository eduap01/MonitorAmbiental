from sqlalchemy.orm import Session
from models.Sensor import Sensor
import uuid

def create_sensor(db: Session, nombre: str):
    nuevo_uuid = uuid.uuid4()
    db_sensor = Sensor(id=nuevo_uuid, nombre=nombre)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor