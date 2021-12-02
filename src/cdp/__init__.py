import lvgl as lv
import ujson as json
from ili9XXX import ili9341
from machine import Pin, ADC, reset
from utime import sleep_ms, sleep

# ===== Inicializar variables ===== #
sensor_us = None
uart = None
fsm = None
group = None
scr = None

# ===== CONFIGURACION PROGRAMA ===== #
_global_config = {}

# ===== LISTA DE USUARIOS ===== #
_users_list = []

from cdp.classes import Sensor_US, ControlUART, Usuario, StateMachine

# ===== OBJETOS DE CONTROL ===== #
sensor_us = Sensor_US(16, 36)
uart = ControlUART(9600, 17, 34)
fsm = StateMachine()

# Corregir error de lectura
uart.dummy_read_correction(
    dummy_tries = 2,
    wait_ms = 1000
)

# ===== PINES ===== #
turn_counter = Pin(35, Pin.IN)

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

# ===== LVGL ===== #
lv.init()
display = ili9341(mosi=23, miso=19, clk=18, dc=21, cs=5, rst=22, power=-1, backlight=-1)

class Joystick:
    last_key = ""

    def __init__(self):
        self.key = lv.KEY.ENTER
        self.state = lv.INDEV_STATE.RELEASED

        self.r_key = lv.KEY.LEFT
        self.l_key = lv.KEY.RIGHT

    def read_cb(self, drv, data):
        r = uart.send_and_receive("askswi")
        if r:
            r = r.split('-')
            read = int(r[0])
            press = int(r[2])
            print(press, read)
            this_key = ""

            if read > 700:
                self.next(lv.INDEV_STATE.PRESSED)
                this_key = "right"
            elif read < 50:
                self.prev(lv.INDEV_STATE.PRESSED)
                this_key = "left"
            elif press == 0:
                self.enter(lv.INDEV_STATE.PRESSED)
                this_key = "enter"
            else:
                if self.last_key == "right":
                    self.next(lv.INDEV_STATE.RELEASED)
                elif self.last_key == "left":
                    self.prev(lv.INDEV_STATE.RELEASED)
                elif self.last_key == "enter":
                    self.enter(lv.INDEV_STATE.RELEASED)

            data.key = self.key
            data.state = self.state
            self.last_key = this_key
            return False

    def send_key(self, event, key):
        self.key = key
        self.state = event

    def next(self, event):
        self.send_key(event, self.r_key)

    def prev(self, event):
        self.send_key(event, self.l_key)

    def enter(self, event):
        self.send_key(event, lv.KEY.ENTER)

joystick = Joystick()
indev = lv.indev_drv_t()
indev.init()
indev.type = lv.INDEV_TYPE.ENCODER
indev.read_cb = joystick.read_cb
encoder = indev.register()

group = lv.group_create()
encoder.set_group(group)

scr = lv.obj()

# ===== FUNCIONES ===== #
def load_config_from_file_global():
    try:
        with open("cdp/settings/cdp_config.json", "r") as file:
            _global_config = json.load(file)
        return _global_config
    except OSError:
        print("cdp_config.json is missing. Creating a new default one...")
        with open("cdp/settings/cdp_config.json", "w") as file:
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
        with open("cdp/settings/motor_data.json", "w") as file:
            c = {
                "Actuales" : {
                    "cabezal" : 0,
                    "apbrazo" : 0,
                    "lumbar" : 0,
                    "assdepth" : 0,
                    "assheight" : 0
                }
            }
            json.dump(c, file)
        return load_users_from_file_global()

def set_motorpin_output():
    for pin_list in motor_pines.values():
        for value in pin_list.values():
            for index, pin in enumerate(value):
                value[index] = Pin(pin, Pin.OUT)

# ===== INIT ===== #
_global_config = load_config_from_file_global()
_users_list = load_users_from_file_global()
set_motorpin_output()
