from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Routers
from api.medicion_endpoints import router as medicion_router
from api.sensor_endpoints import router as sensor_router
from api.ubicacion_endpoints import router as ubicacion_router

# Archivo principal de la aplicación FastAPI
# Registra las rutas de la API y sirve el frontend

# Incluir endpoints de distintas funcionalidades agrupadas


app = FastAPI()

# Incluir rutas de API
app.include_router(medicion_router, prefix="/api")
app.include_router(sensor_router, prefix="/api")
app.include_router(ubicacion_router, prefix="/api")

# Montar archivos estáticos (JS, CSS, HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta raíz que sirve el HTML del dashboard
@app.get("/")
def serve_dashboard():
    return FileResponse("static/dashboard.html")


