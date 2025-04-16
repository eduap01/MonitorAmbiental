
# Configuración básica de conexión a PostgreSQL
# Para scripts independientes que no usan SQLAlchemy (ej: exportar_datos.py)

DATABASE_CONFIG = {
    "dbname": "monitoreo_ambiental",
    "user": "postgres",
    "password": "1",
    "host": "localhost",
    "port": "5432"
}
