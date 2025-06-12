from sqlalchemy.orm import Session
from models.Sensor import Sensor


#Parte descartada del proyecto. Ahora no tiene funcionalidad

# Inserta un nuevo sensor en la base de datos con UUID.
# Se utiliza al inicializar el sistema o añadir sensores nuevos.
def create_sensor(db: Session, nombre: str, tipo: str):
    db_sensor = Sensor(nombre=nombre, tipo=tipo)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

