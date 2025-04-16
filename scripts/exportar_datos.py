import pandas as pd
from sqlalchemy import create_engine

# Configura la URL de tu base de datos
DATABASE_URL = 'postgresql://postgres:1@localhost:5432/monitoreo_ambiental'

# Conexión con SQLAlchemy
engine = create_engine(DATABASE_URL)

# Consulta SQL
query = """
SELECT fecha_hora, temperatura, humedad, presion
FROM mediciones
ORDER BY fecha_hora ASC
"""

# Ejecutar la consulta y exportar a CSV
df = pd.read_sql(query, engine)
df.to_csv('scripts/mediciones.csv', index=False)

print("✅ Datos exportados a scripts/mediciones.csv")
