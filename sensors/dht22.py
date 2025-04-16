import random

class DHT22:
    def leer_temperatura(self):
        return round(random.uniform(15, 25), 2)  # Simulación de temperatura


    def leer_humedad(self):
        return round(random.uniform(900, 1100), 2)
