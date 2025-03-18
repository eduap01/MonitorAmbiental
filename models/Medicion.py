from sqlalchemy import Column, Integer, Numeric, DateTime
from database import Base

class Medicion(Base):
    __tablename__ = 'mediciones'

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    temperatura = Column(Numeric(5, 2), nullable=False)
    humedad = Column(Numeric(5, 2), nullable=False)
    calidad_aire = Column(Numeric(5, 2), nullable=False)
    presion = Column(Numeric(7, 2), nullable=False)