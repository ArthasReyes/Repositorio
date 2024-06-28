from machine import Pin, ADC
from neoeduca import Movil, ADS1115
import time

#Motores
autito = Movil(1,2,4,5)
ads = ADS1115(sda_pin=14, scl_pin=15)
#sensores QTI
qti_pines = [0, 1, 2, 3]  # Pines de los sensores QTI en el I2C
umbrales = [2000, 2000, 2000, 2000] #calibrar

# Casos posibles: 0 blanco, 1 negro
acciones = {
    (0, 0, 0, 0): autito.avanzar,
    (1, 0, 0, 0): autito.izquierda,
    (1, 1, 0, 0): autito.izquierda,
    (0, 0, 1, 0): autito.derecha,
    (0, 0, 1, 1): autito.derecha,
    (1, 0, 1, 1): autito.avanzar,
}

while True:

    sensores_valores = [ads.leer(0,pin) for pin in qti_pines]

    detecciones = tuple(int(valor > umbral) for valor, umbral in zip(sensores_valores, umbrales))
    print(detecciones)
    accion = acciones.get(detecciones, autito.detener)

    accion()
    time.sleep(0.1)
