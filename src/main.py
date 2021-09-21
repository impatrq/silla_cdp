# main.py
import _thread as thr
import json as json
import machine
from machine import Pin, ADC
import cdp_helper as helper
#import cdp_gui as gui
from cdp_user import Usuario
from cdp_fsm import StateMachine

# Lista de hilos
available_threads = {}

# Estados para la FSM
STARTING, IDLE, CALIBRATING, SENSOR_READING, USER_SCREEN = range(5)

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
        print("cdp_config.json is missing. Creating a new default one...")
        with open("settings/cdp_config.json", "w") as file:
            c = {
                "first_time_open" : True
            }
            json.dump(c, file)
        return load_config_from_file_global()


def load_users_from_file_global():
    new_list = []

    try:
        with open("settings/motor_data.json", "r") as file:
            data = json.load(file)
        for user, config in data.items():
            if user == "Actuales":
                continue
            new_list.append(Usuario(user, config))
        return new_list
    except OSError:
        print("motor_data.json is missing. Creating a new default one...")
        with open("settings/motor_data.json", "w") as file:
            c = {
                "Actuales" : {
                    "cabezal" : 0,
                    "apbrazo" : 0,
                    "lumbar" : 0,
                    "assprof" : 0,
                    "assheight" : 0
                }
            }
            json.dump(c, file)
        return load_users_from_file_global()

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

# def listen_for_shutdown(pin: Pin):
#     # Dependiendo de como salgan las pruebas del reset, esta condicion podría moverse al principio del programa.
#     if machine.wake_reason() == machine.PIN_WAKE:
#         # TODO: Aca iría el codigo luego de despertar.
#         return

#     # TODO: Acá iría el codigo previo a la suspensión...
#     machine.lightsleep()

def StartDefault():
    try:
        # Probablemente cambie en el futuro para albergar mas de un helper thread a la vez
        available_threads['helper_thread'] = thr.start_new_thread(helper.return_to_default, (motor_pines['atras'], pin_sensor))
    except thr.error as e:
        print("[Err #001] Error al intentar iniciar un hilo.\n" + e)

def wait_for_action():
    # TODO: interacción con la GUI
    print(".")
    fsm.next_state()

def main():
    # Establecer entradas y salidas
    #set_motorpin_output()
    #set_sensorpin_input()

    if _global_config["first_time_open"]:
        # TODO: Bienvenida por la GUI + primera calibracion
        print("Bienvenido a Silla CDP")
        _global_config["first_time_open"] = False
    # TODO: Carga de pantalla inicial por la GUI
    print("Pantalla de usuarios")

    # Cambiar de estado a espera
    fsm.State = IDLE

# Instancia de la FSM
fsm = StateMachine((STARTING, main))

if __name__ == "__main__":
    # Cargar datos desde archivos (se hace desde aca para modificar la variable global)
    _global_config = load_config_from_file_global()
    _users_list = load_users_from_file_global()

    # Agregar estados a la FSM
    fsm.add_states([
        (IDLE, wait_for_action)
    ])

    # Arrancar la FSM
    fsm.start()

    # Poner interrupción en el pin de apagado
    # pin_off.irq(handler = listen_for_shutdown, trigger = Pin.IRQ_FALLING, wake = machine.DEEPSLEEP or machine.SLEEP)

    # Correr modulo GUI en la primera pantalla
    # available_threads['gui_thread'] = thr.start_new_thread(gui.AbrirVentana, ())

    # Los hilos no corren si se termina el programa principal (implementar luego detener hilos desde este script)
    while True:
        i = input()
        if i == "stop":
            break
