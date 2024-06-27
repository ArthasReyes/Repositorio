# Programa principal
from machine import Pin, ADC
import time
from movil import Movil_2_ruedas

autito = Movil_2_ruedas(0, 1, 4, 5)
autito.calibrar(15, 16)

try:
    while True:
        vel = input(" que velocidad quiere?")
        autito._velocidad = int(vel)
        autito.avanzar()
    
except:
    autito.detener()