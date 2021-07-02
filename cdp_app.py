import RPi.GPIO as gpio
import cdp_default as default
import cdp_gui as gui
import threading

# Variables de pines
# Provisional...?
pin_sensor = 32
motor_pines = {
    'pin_adelante' : 29,
    'pin_atras' : 31,
    'pin_enable_cabezal' : 33,
    'pin_enable_apbrazo1' : 35,
    'pin_enable_apbrazo2' : 37,
    'pin_enable_lumbar' : 36,
    'pin_enable_assdepth' : 38,
    'pin_enable_assheight' : 40
}

def set_motorpin_output():
        for pin in motor_pines.values():
            gpio.setup(pin, gpio.OUT)
            pass

def Say(text):
    print(text)

def StartDefault():
    t = threading.Thread(target=default.return_to_default, args=(motor_pines['pin_atras'], pin_sensor))
    t.start()

# Establecer entradas y salidas
gpio.setmode(gpio.BOARD)
gpio.setup(pin_sensor, gpio.IN)
set_motorpin_output()

if __name__ == "__main__":
    gui_thread = threading.Thread(target = gui.AbrirVentana)
    gui_thread.start()

# Ver donde acomodar a futuro
gpio.cleanup()