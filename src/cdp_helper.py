# Modulo con funciones auxiliares para silla CDP
import json
import cdp_gui as gui
from machine import Pin, ADC

# Macros
ADC_THRESHOLD = 512

# Función para obtener una lectura de ADC y transformarla a estado lógico.
def adc_check_threshold(pin: ADC, minim: int = 0, maxim: int = 1023) -> bool:
    # Establecer rango máximo como 3.3V y valores de 0 a 1023
    pin.atten(ADC.ATTN_11DB)
    pin.width(ADC.WIDTH_10BIT)

    return maxim > pin.read() > minim

def adc_update_all_states(sensor_pines: dict, v_update: bool = False) -> bool:
    well_sit_cond = len(sensor_pines)
    i = 0

    # Poner verdadero o falso en el dict de sensores segun si pasan el umbral o no.
    for pin in sensor_pines.values():
        val = adc_check_threshold(pin[0], minim=ADC_THRESHOLD)
        pin[1] = val
        i += int(val)
    
    # Si se le pasa este parámetro, llamar a la funcion para actualizar la pantalla.
    if v_update:
        #TODO: Provisional hasta tener la verdadera funcion
        gui.update_sensor_state()

    return True if (i >= well_sit_cond) else False

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