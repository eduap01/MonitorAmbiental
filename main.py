from fastapi import FastAPI
from api.medicion_endpoints import router as medicion_router
from api.registro_endpoints import router as registro_router  # Importación corregida
from api.sensor_endpoints import router as sensor_router

app = FastAPI()

app.include_router(medicion_router, prefix="/api")
app.include_router(registro_router, prefix="/api")  # Asegúrate de que esto esté presente
app.include_router(sensor_router, prefix="/api")



@app.get("/")
def read_root():
    return {"Hello": "World"}