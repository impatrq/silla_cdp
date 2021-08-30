# main.py
import _thread as thr
import machine
from machine import Pin
import cdp_helper as helper
import cdp_gui as gui

# Lista de hilos
available_threads = {}

# Variables de pines
pin_sensor = Pin(32, Pin.IN, Pin.PULL_UP)
pin_off = Pin(9, Pin.IN, Pin.PULL_UP)       # Establecido como el que usabamos anteriormente (#TODO: cambiar pines)

#TODO: Reemplazar numero de pines por los correctos.
sensor_pines = {
    'adelante' : [1, False, 0, 1023],
    'atras' : [1, False, 0, 1023],
    'cabezal' : [1, False, 0, 1023],
    'apbrazo' : [1, False, 0, 1023],
    'lumbar' : [1, False, 0, 1023],
    'assdepth' : [1, False, 0, 1023],
    'assheight' : [1, False, 0, 1023]
}

#TODO: Arreglar pines de motores (cantidad de pines y de motores)
# Solucion temporal hasta verificar una posibilidad de placa puente-h
motor_pines = {
    'adelante' : [29],
    'atras' : [31],
    'cabezal' : [33],
    'apbrazo' : [35, 37],
    'lumbar' : [36],
    'assdepth' : [38],
    'assheight' : [40]
}

def set_motorpin_output():
    for value in motor_pines.values():
        for index, pin in enumerate(value):
            value[index] = Pin(pin, Pin.OUT, Pin.PULL_DOWN, 0)

def listen_for_shutdown(pin: Pin):
    # Dependiendo de como salgan las pruebas del reset, esta condicion podría moverse al principio del programa.
    if machine.wake_reason() == machine.PIN_WAKE:
        # TODO: Aca iría el codigo luego de despertar.
        return

    # TODO: Acá iría el codigo previo a la suspensión...
    machine.lightsleep()

def StartDefault():
    try:
        # Probablemente cambie en el futuro para albergar mas de un helper thread a la vez
        available_threads['helper_thread'] = thr.start_new_thread(helper.return_to_default, (motor_pines['atras'], pin_sensor))
    except thr.error as e:
        print("[Err #001] Error al intentar iniciar un hilo.\n" + e)

# Establecer entradas y salidas
set_motorpin_output()

if __name__ == "__main__":
    # Poner interrupción en el pin de apagado
    pin_off.irq(handler = listen_for_shutdown, trigger = Pin.IRQ_FALLING, wake = machine.DEEPSLEEP or machine.SLEEP)

    # Correr modulo GUI en la primera pantalla
    available_threads['gui_thread'] = thr.start_new_thread(gui.AbrirVentana, ())

    # Los hilos no corren si se termina el programa principal (implementar luego detener hilos desde este script)
    while True:
        i = input()
        if i == "stop":
            break
