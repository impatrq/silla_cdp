# main.py
import _thread as thr
import json as json
from machine import Pin, ADC
import cdp_helper as helper
#import cdp_gui as gui
from cdp_user import Usuario
from cdp_fsm import StateMachine

# Estados para la FSM
STARTING, IDLE, CALIBRATING, SENSOR_READING, USER_SCREEN = range(5)

# Variables de pines
pines_encoder = [22, 1, 3, 21]

#TODO: Reemplazar numero de pines por los correctos.
sensor_pines = {
    'bar' : [1, False, 0, 1023],
    'cabezal' : [1, False, 0, 1023],
    'apbrazo' : [1, False, 0, 1023],
    'lumbar' : [1, False, 0, 1023],
    'assdepth' : [1, False, 0, 1023],
    'assheight' : [1, False, 0, 1023]
}

# Pines de los motores
motor_pines = {
    'cabezal_adelante' : [32],
    'apbrazo_adelante' : [33, 25],
    'assdepth_adelante' : [14],
    'assheight_adelante' : [0],
    'cabezal_atras' : [33],
    'apbrazo_atras' : [25, 27],
    'assdepth_atras' : [12],
    'assheight_atras' : [15]
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

def wait_for_action():
    # TODO: interacción con la GUI
    print(".")
    fsm.next_state()

def main():
    # Establecer entradas y salidas
    set_motorpin_output()
    set_sensorpin_input()

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
