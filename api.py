from fastapi import FastAPI
from pydantic import BaseModel
from models.lectura import guardar_lectura
from fastapi import FastAPI, HTTPException
from models.lectura import obtener_lectura

app = FastAPI()

class LecturaRequest(BaseModel):
    sensor_id: int
    tipo: str
    valor: float

@app.post("/lectura/")
async def recibir_lectura(lectura: LecturaRequest):
    # Llamar a la función que guarda la lectura en la base de datos
    guardar_lectura(lectura.sensor_id, lectura.tipo, lectura.valor)
    return {"mensaje": "Lectura recibida y guardada correctamente."}

# Endpoint para obtener la lectura por sensor_id y tipo
@app.get("/obtener_lectura/{sensor_id}/{tipo}")
async def obtener_lectura_por_id(sensor_id: int, tipo: str):
    lectura = obtener_lectura(sensor_id, tipo)
    if lectura:
        return {"sensor_id": sensor_id, "tipo": tipo, "valor": lectura[0], "fecha_hora": lectura[1]}
    else:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")

