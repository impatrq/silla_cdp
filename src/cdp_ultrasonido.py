from machine import Pin, time_pulse_us
import utime as time

class Sensor_US:
    def __init__(self, trigger_pin: int, echo_pin: int, echo_timeout_us: int = 30000):
        """
            Clase especializada para la lectura del sensor ultrasonido.

            Args:
            `trigger_pin`: numero del pin de trigger.
            `echo_pin`: numero del pin de echo (debe estar protegido con resistencia de 1K).
            `echo_timeout_us`: timeout en microsegundos para la lectura del pulso.
        """
        self.__echo_timeout_us = echo_timeout_us

        self.__trigger = Pin(trigger_pin, Pin.OUT)
        self.__trigger.value(0)

        self.__echo = Pin(echo_pin, Pin.IN)

    def send_pulse_value(self):
        """
            Envia un pulso del `trigger` y luego lee la duracion del pulso del `echo` y la devuelve.
        """
        self.__trigger.value(0)
        time.sleep_us(5)
        self.__trigger.value(1)
        time.sleep_us(10)
        self.__trigger.value(0)

        try:
            pulse_time = time_pulse_us(self.__echo, 1, self.__echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range') from ex
            raise ex

    def send_pulse_centimeters(self):
        """
            Hace una lectura estandar del pulso de `echo` y usa la formula para convertir la lectura a centimetros.
        """
        lectura = self.send_pulse_value()
        return (lectura / 2) / 29.1
