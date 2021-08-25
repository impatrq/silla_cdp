# Modulo con funciones auxiliares para silla CDP
import json
import cdp_gui as gui
from machine import Pin, ADC

# Macros
ADC_THRESHOLD = 512

# Función para obtener una lectura de ADC y transformarla a estado lógico.
def adc_check_threshold(pin: ADC) -> bool:
    # Establecer rango máximo como 3.3V y valores de 0 a 1023
    pin.atten(ADC.ATTN_11DB)
    pin.width(ADC.WIDTH_10BIT)

    return pin.read() > ADC_THRESHOLD

# Versión trucha de wait_for_edge (quizás provisional)
def wait_for_interrupt(pin: Pin):
    while True:
        if pin.value() == 1:
            break

# Función para obtener los datos de los motores
def load_json() -> dict:
    with open("motor_data.json", "r") as file:
        dict_motores = json.load(file)
        file.close()
    return dict_motores

# Funcion para guardar los datos de los motores
def save_json(data: dict):
    with open("motor_data.json", "w") as outfile:
        json.dump(data, outfile, indent = 4)
        outfile.close()

def start_calibration():
    # Mostrar instruccion en pantalla
    # Esperar por presion en varilla
    # Por cada motor...
    #   Mostrar instruccion
    #   Encender motor
    #   Contar pulsos/vueltas del motor
    #   Esperar respuesta del sensor
    #   Detener motor
    #   Guardar en dict con posiciones
    # Devolver dict con posiciones
    return

# Función para mover los motores
def return_to_default(motor_pines: dict, pin_atras: Pin, pin_sensor: Pin):
    dict_motores = load_json()

    for motor in dict_motores['Actuales']:
        # Sacar posicion del motor
        ciclos = dict_motores['Actuales'][motor]

        # Poner en alto los pines enable
        for pin in motor_pines[motor]:
            pin.value(1)

        # Hacer andar el motor hasta terminar los ciclos
        while ciclos > 0:
            gui.motor_values[motor] = True
            pin_atras.value(1)
            wait_for_interrupt(pin_sensor)
            pin_atras.value(0)
            ciclos -= 1
        
        # Poner en bajo todos los pines enable
        for pin in motor_pines[motor]:
            pin.value(0)

        # Indicarle al modulo GUI que el motor ya no se está moviendo
        gui.motor_values[motor] = False

        # Guardar nueva posicion de este motor
        dict_motores['Actuales'][motor] = ciclos
    
    # Guardar nueva posicion de los motores
    save_json(dict_motores)

# Para pruebas
if __name__ == "__main__":
    dict_prueba = {
        "Actuales" : {
            "cabezal" : 1,
            "apbrazo" : 2,
            "lumbar" : 3,
            "assprof" : 4,
            "assheight" : 3
        }
    }

    save_json(dict_prueba)