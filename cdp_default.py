# Modulo return_to_default helper para silla CDP
import json
import RPi.GPIO as gpio

# No se si vá si o si, o si no
# gpio.setmode(gpio.BOARD)

# Función para obtener los datos de los motores
def load_json() -> dict:
    with open("motor_data.json", "r") as file:
        dict_motores = json.load(file)
        file.close()
    return dict_motores['Actuales']

# Funcion para guardar los datos de los motores
def save_json(data: dict):
    with open("motor_data.json", "w") as outfile:
        json.dump(data, outfile, indent = 4)
        outfile.close()

# Función para mover los motores
def return_to_default(pin_atras: int, pin_sensor: int):
    dict_motores = load_json()

    for motor in dict_motores:
        # Sacar posicion del motor
        ciclos = dict_motores[motor][0]

        # Poner en alto los pines enable
        gpio.output(dict_motores[motor][1], True)

        # Hacer andar el motor hasta terminar los ciclos
        while ciclos > 0:
            gpio.output(pin_atras, True)
            gpio.wait_for_edge(pin_sensor, gpio.FALLING)
            gpio.output(pin_atras, False)
            ciclos -= 1
        
        # Poner en bajo todos los pines enable
        gpio.output(dict_motores[motor][1], False)

        # Guardar nueva posicion de este motor
        dict_motores[motor][0] = ciclos
    
    # Guardar nueva posicion de los motores
    save_json(dict_motores)
