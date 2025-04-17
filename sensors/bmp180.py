import random

#Utilizada en la primera fase para simluar registros. Ahora no tiene funcionalidad

class BMP180:
    def leer_temperatura(self):
        return round(random.uniform(15, 25), 2)

    def leer_presion(self):
        return round(random.uniform(900, 1100), 2)