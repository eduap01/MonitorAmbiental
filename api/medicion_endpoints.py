from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from metodos.medicion_crud import create_medicion
from models.Medicion import Medicion as MedicionModel
from pydantic_models.MedicionPydantic import MedicionCreate, Medicion  # Importar desde el directorio schemas
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mediciones/", response_model=Medicion)
def create_medicion_endpoint(medicion: MedicionCreate, db: Session = Depends(get_db)):
    db_medicion = create_medicion(db, medicion)
    return db_medicion


#@app.post("/mediciones/")
#async def recibir_medicion(medicion: Medicion):
    # Aquí se procesan los datos que la Raspberry Pi envió
 #   print(f"Datos recibidos - Temperatura: {medicion.temperatura}°C, Humedad: {medicion.humedad}%")

    # Puedes guardar estos datos en la base de datos o realizar otras acciones
 #   return {"status": "Datos recibidos correctamente"}
