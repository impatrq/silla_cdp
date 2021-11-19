import lvgl as lv
import ujson as json
from ili9XXX import ili9341
from machine import Pin
from cdp.classes import Sensor_US, ControlUART, Usuario
from cdp.gui import read_joystick_cb

# ===== FSM STATES ===== #
STARTING, IDLE, CALIBRATING, SENSOR_READING, USER_SCREEN = range(5)

# ===== CONTROL US Y UART ===== #
sensor_us = Sensor_US(16, 36)
uart = ControlUART(9600, 17, 34)

# ===== PINES ===== #
pin_encoder = 35

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

# ===== CONFIGURACION PROGRAMA ===== #
_global_config = {}

# ===== LISTA DE USUARIOS ===== #
_users_list = []

# ===== LVGL ===== #
lv.init()
display = ili9341(mosi=23, miso=19, clk=18, dc=21, cs=5, rst=22, power=-1, backlight=-1)

indev = lv.indev_drv_t()
indev.init()
indev.type = lv.INDEV_TYPE.ENCODER
indev.read_cb = read_joystick_cb
joystick = indev.register()

group = lv.group_create()
lv.indev_t.set_group(joystick, group)

scr = lv.obj()
lv.scr_load(scr)

# ===== FUNCIONES ===== #
def load_config_from_file_global():
    try:
        with open("settings/cdp_config.json", "r") as file:
            _global_config = json.load(file)
        return _global_config
    except OSError:
        print("cdp_config.json is missing. Creating a new default one...")
        with open("settings/cdp_config.json", "w") as file:
            c = {
                "first_time_open" : True,
                'calibration_data' : {
                    "assheight" :   ['TBD', ['piezo', ["as1", 0, 1023], ["as2", 0, 1023]], '000', 1024],
                    "assdepth" :    ['TBD', ['piezo', ["lu1", 0, 1023], ["lu2", 0, 1023]], '001', 1024],
                    "lumbar" :      ['TBD', ['piezo', ["lu1", 0, 1023], ["lu2", 0, 1023]], '010', 1024],
                    "cabezal" :     ['TBD', ['ultra'], '011', 1024],
                    "apbrazo" :     ['TBD', ['pin', ["apb", 0, 1023], ["as2", 0, 1023]], '100', 1024]
                }
            }
            json.dump(c, file)
        return load_config_from_file_global()

def load_users_from_file_global():
    new_list = []

    try:
        with open(Usuario.json_motor_path, "r") as file:
            data = json.load(file)
        with open(Usuario.json_user_path, 'r') as file:
            icons = json.load(file)
        for user, config in data.items():
            if user == "Actuales":
                continue
            new_list.append(Usuario(user, icons[user], config))
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
    for pin_list in motor_pines.values():
        for value in pin_list.values():
            for index, pin in enumerate(value):
                value[index] = Pin(pin, Pin.OUT, Pin.PULL_DOWN, 0)

# ===== INIT ===== #
_global_config = load_config_from_file_global()
_users_list = load_users_from_file_global()
set_motorpin_output()
