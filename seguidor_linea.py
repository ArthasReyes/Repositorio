from machine import Pin, ADC
from movil import Movil_2_ruedas

#Motores
autito = Autito(motorA1_pin=1, motorA2_pin=2, motorB1_pin=4, motorB2_pin=5)


#sensores QTI
qti_pines = [34, 35, 32, 33]  # Pines de los sensores IR
umbrales = [2000, 2000, 2000, 2000] #calibrar
sensores = [ADC(Pin(pin)) for pin in sensores_pines]

# Casos posibles: 0 blanco, 1 negro
acciones = {
    (0, 0, 0, 0): autito.adelante,
    (1, 0, 0, 0): autito.izquierda,
    (1, 1, 0, 0): autito.izquierda,
    (0, 0, 1, 0): autito.derecha,
    (0, 0, 1, 1): autito.derecha,
}


while True:
    sensores_valores = [sensor.read() for sensor in sensores]

    detecciones = tuple(int(valor > umbral) for valor, umbral in zip(sensores_valores, umbrales))

    accion = acciones.get(detecciones, detener)
    accion()

    time.sleep(0.1)
