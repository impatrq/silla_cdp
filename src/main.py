# main.py
import _thread as thr
import machine
from machine import Pin, ADC
import cdp_helper as helper
import cdp_gui as gui
import json as json

# Lista de hilos
available_threads = {}

# Variables de pines
pin_sensor = Pin(32, Pin.IN, Pin.PULL_UP)
pin_off = Pin(9, Pin.IN, Pin.PULL_UP)       # Establecido como el que usabamos anteriormente (#TODO: cambiar pines)

#TODO: Reemplazar numero de pines por los correctos.
sensor_pines = {
    'bar' : [1, False, 0, 1023],
    'cabezal' : [1, False, 0, 1023],
    'apbrazo' : [1, False, 0, 1023],
    'lumbar' : [1, False, 0, 1023],
    'assdepth' : [1, False, 0, 1023],
    'assheight' : [1, False, 0, 1023]
}

#TODO: Arreglar pines de motores (cantidad de pines y de motores)
# Solucion temporal hasta verificar una posibilidad de placa puente-h
motor_pines = {
    'cabezal' : [33],
    'apbrazo' : [35, 37],
    'lumbar' : [36],
    'assdepth' : [38],
    'assheight' : [40]
}

# Aca se guardan los datos obtenidos del archivo "cdp_config.json"
_global_config = {}

# Aca se guardan las instancias de clase Usuario obtenidas desde motor_data.json
_users_list = []

def load_config_from_file_global():
    try:
        with open("settings/cdp_config.json", "r") as file:
            _global_config = json.load(file)
        return _global_config
    except OSError:
        print("cdp_config.json is missing. Creating a new one...")
        with open("src/settings/cdp_config.json", "w") as file:
            c = {
                "first_time_open" : True
            }
            json.dump(c, file)


def load_users_from_file_global():
    pass

def set_motorpin_output():
    for value in motor_pines.values():
        for index, pin in enumerate(value):
            value[index] = Pin(pin, Pin.OUT, Pin.PULL_DOWN, 0)

def set_sensorpin_input():
    for value in sensor_pines.values():
        for index, pin in enumerate(value):
            if index == 0:
                value[index] = ADC(Pin(pin, Pin.IN, Pin.PULL_DOWN))
                value[index].atten(ADC.ATTN_11DB)    # Rango maximo 3.3V
                value[index].width(ADC.WIDTH_10BIT)  # Lectura 0-1023

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

def main():
    # Establecer entradas y salidas
    set_motorpin_output()
    set_sensorpin_input()

if __name__ == "__main__":
    # Cargar datos desde archivos (se hace desde aca para modificar la variable global)
    _global_config = load_config_from_file_global()
    load_users_from_file_global()

    main()

    # Poner interrupción en el pin de apagado
    # pin_off.irq(handler = listen_for_shutdown, trigger = Pin.IRQ_FALLING, wake = machine.DEEPSLEEP or machine.SLEEP)

    # Correr modulo GUI en la primera pantalla
    # available_threads['gui_thread'] = thr.start_new_thread(gui.AbrirVentana, ())

    # Los hilos no corren si se termina el programa principal (implementar luego detener hilos desde este script)
    while True:
        i = input()
        if i == "stop":
            break
