from machine import Pin
import cdp_helper as helper
import cdp_gui as gui
import _thread as thr

# Lista de hilos
available_threads = {}

# Variables de pines
pin_sensor = Pin(32, Pin.IN, Pin.PULL_UP)
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
    for key in motor_pines:
        for pin in range(len(motor_pines[key])):
            motor_pines[key][pin] = Pin(motor_pines[key][pin], Pin.OUT, Pin.PULL_DOWN, 0)

def StartDefault():
    try:
        # Probablemente cambie en el futuro para albergar mas de un helper thread a la vez
        available_threads['helper_thread'] = thr.start_new_thread(helper.return_to_default, (motor_pines['atras'], pin_sensor))
    except thr.error as e:
        print("[Err #001] Error al intentar iniciar un hilo.\n" + e)

# Establecer entradas y salidas
set_motorpin_output()

if __name__ == "__main__":
    available_threads['gui_thread'] = thr.start_new_thread(gui.AbrirVentana, ())

    # Los hilos no corren si se termina el programa principal (implementar luego detener hilos desde este script)
    while True:
        i = input()
        if i == "stop":
            break