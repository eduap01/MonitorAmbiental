import psycopg2
from config import DATABASE_CONFIG

def conectar_bd():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
