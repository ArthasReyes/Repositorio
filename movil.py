from machine import Pin, PWM
import time

global contador

def callback_A(encoder):
    global contador_A
    contador_A +=1
    
def callback_B(encoder):
    global contador_B
    contador_B +=1
    
def callback_pass(encoder):
    pass

class Error_velocidad_invalido(Exception):
    pass

class Error_diametro_invalido(Exception):
    pass

class Error_sentido_invalido(Exception):
    pass

class Movil_2_ruedas:
    def __init__(self, motor_A1_pin, motor_A2_pin, motor_B1_pin, motor_B2_pin, freq = 1000):
        self.motor_A1 = PWM(Pin(motor_A1_pin), freq=freq)
        self.motor_A2 = PWM(Pin(motor_A2_pin), freq=freq)
        self._sentido_A = 1  # 1 horario, -1 antihorario
        self._velocidades_A = [] #cm/s
        self._dutys_A = [] #cm/s

        self.motor_B1 = PWM(Pin(motor_B1_pin), freq=freq)
        self.motor_B2 = PWM(Pin(motor_B2_pin), freq=freq)
        self._sentido_B = 1  # 1 horario, -1 antihorario
        self._velocidades_B = [] #cm/s
        self._dutys_B = [] #cm/s
        
        self._velocidad = None #cm/s
        self._diametro = 6.5  # en 
    
    def interpolar(self, vel, vels, dutys):
        for i in range(len(vels)-1):
            anterior = vels[i]
            siguiente = vels[i+1]
            print(anterior, siguiente)
            if anterior < vel and vel < siguiente:
                resultado = (vel-anterior)(siguiente-anterior)*(dutys[i+1]-dutys[i])+dutys[i]
                return resultado
        resultado = 512 * 65535 / 1023 
        return resultado
    
    def vel_to_duty(self):
        if self._velocidad is None or not self._velocidades_A:
            duty_A = 512 * 65535 / 1023
            duty_B = 512 * 65535 / 1023
        else:
            duty_A = self.interpolar(self._velocidad, self._velocidades_A, self._dutys_A)
            duty_B = self.interpolar(self._velocidad, self._velocidades_B, self._dutys_B)
        
        return [int(duty_A), int(duty_B)]
        
        
    def avanzar(self, duty_A=None, duty_B=None):
        if duty_A is None and duty_B is None:
            duty_A = int(duty)
            duty_B = int(duty)
        else:
            duty_A, duty_B = self.vel_to_duty()
                    
        self.motor_A1.duty_u16(0 if sentido_A == 1 else duty_A)
        self.motor_A2.duty_u16(duty_A if sentido_A == 1 else 0)
        
        self.motor_B1.duty_u16(duty_B if sentido_B == 1 else 0)
        self.motor_B2.duty_u16(0 if sentido_B == 1 else duty_B)
        
        return [duty_A, duty_B]
 
    def izquierda(self):
        duty_A, duty_B = self.vel_to_duty()
        
        self.motor_A1.duty_u16(0 if sentido_A == 1 else duty_A)
        self.motor_A2.duty_u16(duty_A if sentido_A == 1 else 0)
        
        self.motor_B1.duty_u16(0)
        self.motor_B2.duty_u16(0)
        
        return [duty_A, 0]

    def derecha(self):
        duty_A, duty_B = self.vel_to_duty()
        
        self.motor_A1.duty_u16(0)
        self.motor_A2.duty_u16(0)
        
        self.motor_B1.duty_u16(duty_B if sentido_B == 1 else 0)
        self.motor_B2.duty_u16(0 if sentido_B == 1 else duty_B)

        return [0, duty_B]
    
    def detener(self):
        self.motor_A1.duty_u16(0)
        self.motor_A2.duty_u16(0)
        
        self.motor_B1.duty_u16(0)
        self.motor_B2.duty_u16(0)

        return [0, 0]
    
    def calibrar(self, encoder_A_pin, encoder_B_pin, manual = None, debug=True):
        if manual is not None:
            self._velocidades_A, self._dutys_A, self._velocidades_B, self._dutys_B = manual
            return
        
        # Retorna un arreglo de velocidades para valores entre [0-100] cm/s
        # Calibrados con el Sensor Encoder Velocidad Optica F249
        # Se toman 20 medidas entre 0 y 1023, y los valores intermedios son interpolados
        global contador_A, contador_B
    
        encoder_A = Pin(encoder_A_pin, Pin.IN)
        encoder_B = Pin(encoder_B_pin, Pin.IN)
        
        encoder_A.irq(trigger=Pin.IRQ_FALLING, handler=callback_A)
        encoder_B.irq(trigger=Pin.IRQ_FALLING, handler=callback_B)
        
        for i in range(300, 1000, 50):
            self.avanzar(duty = i*65535 / 1023)
            time.sleep(0.3)
            contador_A=0
            contador_B=0
            time_start = time.ticks_ms()
            time.sleep(0.5)
            self._velocidades_A.append((contador_A/20) *3.1416*6.5/(time.ticks_diff(time.ticks_ms(), time_start)/1000))
            self._velocidades_B.append((contador_B/20) *3.1416*6.5/(time.ticks_diff(time.ticks_ms(), time_start)/1000))
            self._dutys_A.append(i)
            self._dutys_B.append(i)

            if debug:
                print(i, self._velocidades_A[-1], self._velocidades_B[-1])
                
        encoder_A.irq(trigger=Pin.IRQ_FALLING, handler=callback_pass)
        encoder_B.irq(trigger=Pin.IRQ_FALLING, handler=callback_pass)
        
        self.detener()
        
        return [self._velocidades_A, self._dutys_A, self._velocidades_B, self._dutys_B]
    
    
    def sentido(self, sentido_A, sentido_B):
        self.sentido_A = sentido_A
        self.sentido_B = sentido_B
    
    @property
    def velocidad(self):
        return self._velocidad

    @velocidad.setter
    def velocidad(self, value):
        if value is None or value < 0:
            raise Error_velocidad_invalido("La velocidad debe ser positiva, utilizar el sentido del motor en su lugar")
        self._velocidad = value

    @property
    def diametro(self):
        return self._diametro

    @diametro.setter
    def diametro(self, value):
        if value is None or value <= 0 or value > 100:
            raise Error_diametro_invalido("El diámetro considera ruedas de hasta 100 mm (10 cm)")
        self._diametro = value

    @property
    def sentido_A(self):
        return self._sentido_A

    @sentido_A.setter
    def sentido_A(self, value):
        if value is None or value != 1 or value != -1:
            raise Error_sentido_invalido("El sentido debe ser 1 o -1")
        self._sentido_A = value


    @property
    def sentido_B(self):
        return self._sentido_B

    @sentido_B.setter
    def sentido_B(self, value):
        if value is None or value != 1 or value != -1:
            raise Error_sentido_invalido("El sentido debe ser 1 o -1")
        self._sentido_B = value