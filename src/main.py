# main.py
import lvgl as lv
import ujson as json
from machine import Pin
#import cdp_helper as helper
#import cdp_gui as gui
from cdp_classes import Usuario, StateMachine, Sensor_US, ControlUART
from ili9XXX import ili9341

# ==================== VARIABLES GLOBALES==================== #

# Estados para la FSM
STARTING, IDLE, CALIBRATING, SENSOR_READING, USER_SCREEN = range(5)

# Variables de pines
pin_encoder = 35

# Sensor ultrasonido
sensor_us = Sensor_US(16, 36)

# Comunicacion UART con ATMega328P
uart = ControlUART(9600, 17, 34)

# Pines de los motores
motor_pines = {
    "Adelante": {
        'cabezal' : [13],
        'apbrazo' : [4, 15],
        'assdepth' : [14],
        'assheight' : [26],
        'lumbar' : [33]
    },
    "Atras" : {
        'cabezal' : [12],
        'apbrazo' : [2, 0],
        'assdepth' : [27],
        'assheight' : [25],
        'lumbar' : [32]
    }
}

# Aca se guardan los datos obtenidos del archivo "cdp_config.json"
_global_config = {}

# Aca se guardan las instancias de clase Usuario obtenidas desde motor_data.json
_users_list = []

# Inicializar pantalla LCD
lv.init()
disp = ili9341(mosi=23, miso=19, clk=18, dc=21, cs=5, rst=22, power=-1, backlight=-1)

# ==================== FUNCIONES ==================== #

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

# O(n^3) <-- Debe haber una manera de hacerlo mas optimo
def set_motorpin_output():
    for pin_list in motor_pines.values():
        for value in pin_list.values():
            for index, pin in enumerate(value):
                value[index] = Pin(pin, Pin.OUT, Pin.PULL_DOWN, 0)

def wait_for_action():
    # TODO: interacción con la GUI
    print(".")
    fsm.next_state()

def main():
    # Establecer entradas y salidas
    set_motorpin_output()

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
