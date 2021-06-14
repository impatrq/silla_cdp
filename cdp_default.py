# Modulo return_to_default helper para silla CDP
import json
import cdp_gui as gui
# import RPi.GPIO as gpio

# No se si vá si o si, o si no
# gpio.setmode(gpio.BOARD)

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
def return_to_default(pin_atras: int, pin_sensor: int):
    dict_motores = load_json()

    for motor in dict_motores['Actuales']:
        # Sacar posicion del motor
        ciclos = dict_motores['Actuales'][motor][0]

        # Poner en alto los pines enable
        # gpio.output(dict_motores[motor][1], True)

        # Hacer andar el motor hasta terminar los ciclos
        while ciclos > 0:
            gui.motor_values[motor] = True
            # gpio.output(pin_atras, True)
            # gpio.wait_for_edge(pin_sensor, gpio.FALLING)
            # gpio.output(pin_atras, False)
            input("Pasar ciclo")
            print(ciclos)
            ciclos -= 1
        
        # Poner en bajo todos los pines enable
        # gpio.output(dict_motores[motor][1], False)

        gui.motor_values[motor] = False

        # Guardar nueva posicion de este motor
        dict_motores['Actuales'][motor][0] = ciclos
    
    # Guardar nueva posicion de los motores
    save_json(dict_motores)

# Para pruebas
if __name__ == "__main__":
    dict_motores = {
        "Actuales" : {
            "motor_cabezal" : (1, 0),
            "motor_ap" : (2, (0, 0)),
            "motor_lumbar" : (3, 0),
            "motor_assprof" : (4, 0),
            "motor_assheight" : (3, 0)
        }
    }

    save_json(dict_motores)