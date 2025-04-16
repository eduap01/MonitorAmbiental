from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from metodos.medicion_crud import create_medicion
from models.Medicion import Medicion as MedicionModel
from pydantic_models.MedicionPydantic import MedicionCreate, Medicion
from database import SessionLocal
from sqlalchemy import desc

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint POST para crear mediciones
@router.post("/mediciones/", response_model=Medicion)
def create_medicion_endpoint(medicion: MedicionCreate, db: Session = Depends(get_db)):
    db_medicion = create_medicion(db, medicion)
    return db_medicion

#Para sacar todos los registros, pero OJO porque puede colapsar el front

# endpoint GET para listar todas las mediciones
#@router.get("/mediciones/", response_model=list[Medicion])
#def listar_mediciones(db: Session = Depends(get_db)):
#    return db.query(MedicionModel).all()


@router.get("/mediciones/", response_model=list[Medicion])
def listar_mediciones(db: Session = Depends(get_db)):
    return db.query(MedicionModel)\
             .order_by(desc(MedicionModel.fecha_hora))\
             .limit(200)\
             .all()

