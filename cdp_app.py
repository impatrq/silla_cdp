import RPi.GPIO as gpio
import cdp_default as default

# Provisional...?
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

# Helper
def set_motorpin_output():
    for pin in motor_pines.values():
        gpio.setup(pin, gpio.OUT) 

# Establecer entradas y salidas
gpio.setmode(gpio.BOARD)
set_motorpin_output()

# Espacio para resto del codigo...

gpio.cleanup()