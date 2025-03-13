# routes.py
from fastapi import APIRouter
from models.lectura import guardar_lectura, obtener_lecturas  # Asegúrate de tener estas funciones en tu modelo

router = APIRouter()

@router.post("/lectura/")
def crear_lectura(sensor_id: int, tipo: str, valor: float):
    guardar_lectura(sensor_id, tipo, valor)
    return {"message": "Lectura almacenada correctamente"}

@router.get("/lectura/")
def obtener_todas_las_lecturas():
    lecturas = obtener_lecturas()  # Asumiendo que tienes esta función en tu modelo
    return {"lecturas": lecturas}
