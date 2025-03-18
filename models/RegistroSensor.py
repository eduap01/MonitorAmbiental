from sqlalchemy import Integer, String, ForeignKey, Column, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class RegistroSensor(Base):
    __tablename__ = 'registros_sensores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensores.id'))  # Cambiado a Integer
    medicion_id = Column(Integer, ForeignKey('mediciones.id'))
    tipo_medicion = Column(String(50), nullable=False)
    valor = Column(DECIMAL(7, 2), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación con Sensor
    sensor = relationship('Sensor', back_populates='registros')
