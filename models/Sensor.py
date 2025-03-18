from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from database import Base


class Sensor(Base):
    __tablename__ = 'sensores'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Cambiado a INTEGER
    nombre = Column(String(50), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)

    # Relación con registros_sensores (ya no hay UUID, ahora Integer)
    registros = relationship('RegistroSensor', back_populates='sensor')
