from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración y utilidades para la conexión a la base de datos con SQLAlchemy

# URL de conexión (debería ocultarse en entorno de producción)
# Puedes migrarlo a una variable de entorno más adelante si quieres mayor seguridad


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost:5432/monitoreo_ambiental"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()