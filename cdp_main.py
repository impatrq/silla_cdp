# import RPi.GPIO as gpio
import cdp_helper as helper
import cdp_gui as gui
import _thread as thr

# Lista de hilos
available_threads = {}

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
            # gpio.setup(pin, gpio.OUT)
            pass

def Say(text):
    print(text)

def StartDefault():
    try:
        # Probablemente cambie en el futuro para albergar mas de un helper thread a la vez
        available_threads['helper_thread'] = thr.start_new_thread(helper.return_to_default, (motor_pines['pin_atras'], pin_sensor))
    except thr.error as e:
        print("[Err #001] Error al intentar iniciar un hilo.\n" + e)

# Establecer entradas y salidas
# gpio.setmode(gpio.BOARD)
# gpio.setup(pin_sensor, gpio.IN)
set_motorpin_output()

if __name__ == "__main__":
    available_threads['gui_thread'] = thr.start_new_thread(gui.AbrirVentana, ())

    # Los hilos no corren si se termina el programa principal (implementar luego detener hilos desde este script)
    while True:
        i = input()
        if i == "stop":
            break