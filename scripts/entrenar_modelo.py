import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump

# Este script entrena un modelo de regresión lineal para predecir la temperatura futura.

# Carga los datos desde `scripts/mediciones.csv`.
# Crea una columna llamada `temperatura_futura`, que representa la temperatura del siguiente paso temporal.
# Entrena un modelo de regresión lineal usando como entrada:
#   - temperatura actual
#   - humedad actual
#   - presión actual
# Guarda el modelo entrenado en `modelo_temp_rpi.joblib` para ser usado en la Raspberry Pi.

# Ejecutar este script cada vez que se quiera reentrenar el modelo con nuevos datos.


# Cargar los datos
df = pd.read_csv('scripts/mediciones.csv')
df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
df = df.sort_values('fecha_hora')

# Crear la columna con la temperatura futura (+1 paso)
df['temperatura_futura'] = df['temperatura'].shift(-1)
df = df.dropna()

# Variables de entrada (X) y de salida (y)
X = df[['temperatura', 'humedad', 'presion']]
y = df['temperatura_futura']

# Dividir en entrenamiento y prueba (opcional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Guardar el modelo
dump(modelo, 'modelo_temp_rpi.joblib')
print("✅ Modelo entrenado y guardado como modelo_temp_rpi.joblib")
