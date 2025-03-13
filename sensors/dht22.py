import random

class DHT22:
    def __init__(self):
        self.temperatura = 25.0  # Valor inicial de temperatura
        self.humedad = 50.0       # Valor inicial de humedad

    def leer_temperatura(self):
        # Simula una fluctuación pequeña en la temperatura
        self.temperatura += random.uniform(-0.5, 0.5)
        return round(self.temperatura, 2)

    def leer_humedad(self):
        # Simula una fluctuación pequeña en la humedad
        self.humedad += random.uniform(-1, 1)
        return round(self.humedad, 2)