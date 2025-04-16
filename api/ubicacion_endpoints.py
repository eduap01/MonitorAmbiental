from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union


# POST: Guarda ubicación actual recibida desde el frontend.
# GET: Devuelve ubicación actual almacenada al frontend.


router = APIRouter()

class Ubicacion(BaseModel):
    lat: float
    lon: float
    ciudad: str
    pais: str

# Diccionario mutable global
ubicacion_actual = {}

@router.post("/ubicacion/")
def recibir_ubicacion(ubicacion: Ubicacion):
    print(f"Ubicación recibida: {ubicacion}")
    ubicacion_actual.clear()
    ubicacion_actual.update(ubicacion.dict())
    return {"mensaje": "Ubicación recibida"}

@router.get("/ubicacion/", response_model=Union[Ubicacion, dict])
def obtener_ubicacion():
    if ubicacion_actual:
        print(f"Ubicación devuelta al frontend: {ubicacion_actual}")
        return ubicacion_actual
    print("No hay ubicación disponible")
    return {"mensaje": "Ubicación no disponible"}
