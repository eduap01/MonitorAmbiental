from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Sensor(Base):
    __tablename__ = 'sensores'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    ubicacion = Column(String(100), nullable=False)
    fecha_instalacion = Column(DateTime, nullable=False)