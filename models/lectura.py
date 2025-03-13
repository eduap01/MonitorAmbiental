from database import conectar_bd
from datetime import datetime

def guardar_lectura(sensor_id, tipo, valor):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Verificar si el sensor_id existe en la tabla sensores
            cursor.execute("SELECT id FROM sensores WHERE id = %s", (sensor_id,))
            if not cursor.fetchone():
                print(f"Error: El sensor_id={sensor_id} no existe en la tabla sensores.")
                return

            # Preparar el valor de la fecha
            fecha_hora = datetime.now()

            # Crear el diccionario con los tipos de sensor
            tipo_columnas = {
                "temperatura": "temperatura",
                "humedad": "humedad",
                "calidad_aire": "calidad_aire",
                "presion": "presion"
            }

            # Verificar si el tipo es válido
            if tipo not in tipo_columnas:
                print(f"Error: El tipo {tipo} no es válido.")
                return

            # Realizar la inserción de datos
            columna = tipo_columnas[tipo]
            cursor.execute(
                f"INSERT INTO lecturas_sensores (sensor_id, {columna}, fecha_hora) VALUES (%s, %s, %s)",
                (sensor_id, valor, fecha_hora)
            )

            # Confirmar la transacción
            conn.commit()

            print(f"Lectura de {tipo} guardada exitosamente en la base de datos.")

        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")
        finally:
            cursor.close()
            conn.close()



def obtener_lectura(sensor_id, tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Crear el diccionario con los tipos de sensor
            tipo_columnas = {
                "temperatura": "temperatura",
                "humedad": "humedad",
                "calidad_aire": "calidad_aire",
                "presion": "presion"
            }

            # Verificar si el tipo es válido
            if tipo not in tipo_columnas:
                print(f"Error: El tipo {tipo} no es válido.")
                return

            # Realizar la consulta para obtener la última lectura
            columna = tipo_columnas[tipo]
            cursor.execute(
                f"SELECT {columna}, fecha_hora FROM lecturas_sensores WHERE sensor_id = %s ORDER BY fecha_hora DESC LIMIT 1",
                (sensor_id,)
            )
            lectura = cursor.fetchone()

            if lectura:
                valor, fecha_hora = lectura
                print(f"Última lectura de {tipo} del sensor {sensor_id}: {valor} a las {fecha_hora}")
                return valor, fecha_hora
            else:
                print(f"No se encontraron lecturas para el sensor {sensor_id} de tipo {tipo}.")
                return None

        except Exception as e:
            print(f"Error al obtener la lectura de la base de datos: {e}")
        finally:
            cursor.close()
            conn.close()