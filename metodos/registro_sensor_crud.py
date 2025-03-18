# metodos/registro_sensor_crud.py
from sqlalchemy.orm import Session
from models.RegistroSensor import RegistroSensor  # Asumimos que tienes este modelo para los registros
from pydantic_models.RegistroSensorPydantic import RegistroSensorCreate

def create_registro_sensor(db, registro: RegistroSensorCreate):
    db_registro = RegistroSensor(
        sensor_id=registro.sensor_id,  # Asegúrate de que esto sea un Integer
        medicion_id=registro.medicion_id,
        tipo_medicion=registro.tipo_medicion,
        valor=registro.valor,
        fecha_registro=registro.fecha_registro
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro
