# Modulo con funciones auxiliares para silla CDP
import json
from machine import Pin
from utime import sleep_ms
import cdp_gui as gui
from cdp_classes import ControlUART

# ==================== SENSORES ==================== #

def sensor_check_range(comm: ControlUART, which: str, minim: int = 0, maxim: int = 1023) -> bool:
    """
        Pregunta por el sensor 'which' mediante 'comm', luego lo recibe, y si es un numero,
        indica si esta dentro del rango especificado.

        Args:
        `comm`: Objeto de `ControlUART` utilizado para el pedido.
        `which`: string de longitud 3 con el identificador del sensor.
        `minim`: cota inferior no infima del rango.
        `maxim`: cota superior no maxima del rango.
    """
    if len(which) != 3:
        print("Longitud incorrecta. Evitando chequeo.")
        return False
    read = comm.send_and_receive(which)
    try:
        read = int(read)
        return maxim > read > minim
    except ValueError():
        print(read)
        return False

def sensor_check_all_states(comm: ControlUART, sensors: list, v_update: bool = False) -> bool:
    """
        Pregunta por cada sensor dentro de la lista `sensors` mediante 'comm', luego lo recibe, 
        e indica si TODOS estan dentro de su rango especificado.

        Tambien llama a una funcion para actualizar los valores dentro del modulo `cdp_gui`

        Args:
        `comm`: Objeto de `ControlUART` utilizado para el pedido.
        `sensors`: lista con strings de longitud 3 con el identificador del sensor. Formato => [sensor, minimo, maximo]
        `v_update`: bool que indica si llamar o no a la funcion para actualizar visuales.
    """
    well_sit_cond = len(sensors)
    i = 0

    # Formato(sensors) => [ident, minim, maxim]
    for sensor in sensors:
        val = sensor_check_range(comm, sensor[0], minim=sensor[1], maxim=sensor[2])
        i += int(val)

    # Si se le pasa este parámetro, llamar a la funcion para actualizar la pantalla.
    if v_update:
        #TODO: Provisional hasta tener la verdadera funcion
        gui.update_sensor_state()

    return i >= well_sit_cond

def wait_for_interrupt_sensor(comm: ControlUART, which: str):
    """
        Pregunta por el sensor `which` mediante 'comm', cuando recibe algo, sale del bucle.

        Args:
        `comm`: Objeto de `ControlUART` utilizado para el pedido.
        `which`: string de longitud 3 con el identificador del sensor.
    """
    while True:
        if sensor_check_range(comm, which):
            break
        sleep_ms(100)

# ==================== ENCODER ==================== #

def set_select_encoder(comm: ControlUART, value: str):
    """
        Envía el comando para establecer el SELECT del multiplexor. 
        NOTA: no tiene en cuenta si el valor enviado no es un valor binario.

        Args:
        `comm`: Objeto de `ControlUART` utilizado para el pedido.
        `value`: string de longitud 3 con el valor en binario que se desea establecer.
    """
    try:
        if len(value) != 3:
            print("Longitud incorrecta al establecer seleccion MUX")
            return False
        int(value)
        r = comm.send_and_receive(f"mux{value}")
        return r == "ADDRSET"
    except ValueError:
        print("El valor no es un numero al establecer seleccion MUX")
        return False

# ==================== PINES ==================== #

# Versión trucha de wait_for_edge de RPi.GPIO
def wait_for_interrupt(pin: Pin):
    while True:
        if pin.value() == 1:
            break

# ==================== MOTORES ==================== #

# Función para obtener los datos de los motores
def load_json() -> dict:
    with open("settings/motor_data.json", "r") as file:
        dict_motores = json.load(file)
    return dict_motores

# Funcion para guardar los datos de los motores
def save_json(data: dict):
    with open("settings/motor_data.json", "w") as outfile:
        json.dump(data, outfile)

def start_calibration(motor_pines: dict, sensor_pines: dict, turn_counter: Pin):
    # Diccionario con nuevas posiciones
    new_pos = {}

    # Mostrar instruccion en pantalla (placeholder)
    gui.show_calib_instructions('bar')

    # Esperar por presion en varilla
    wait_for_interrupt_adc(sensor_pines['bar'][0], *sensor_pines['bar'][2:])

    # Por cada motor...
    for motor, pines in motor_pines.items():
        # Variable de lista con valores
        pin_sensor_list = sensor_pines[motor]

        # Variable donde guardar la posicion
        pos = 0

        # Mostrar instruccion
        gui.show_calib_instructions(motor)

        # Encender motor
        for pin in pines:
            pin.value(1)

        # Hasta que no este en la posicion correcta...
        while not adc_check_threshold(pin_sensor_list[0], *pin_sensor_list[2:]):
            # Contar pulsos/vueltas del motor
            if turn_counter.value() == 1:
                pos += 1

        # Detener motor al llegar a la posicion correcta
        for pin in pines:
            pin.value(0)

        # Guardar en dict con posiciones
        new_pos[motor] = pos

    # Devolver dict con posiciones
    return new_pos

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
            pin_atras.value(1)
            wait_for_interrupt(pin_sensor)
            pin_atras.value(0)
            ciclos -= 1

        # Poner en bajo todos los pines enable
        for pin in motor_pines[motor]:
            pin.value(0)

        # Guardar nueva posicion de este motor
        dict_motores['Actuales'][motor] = ciclos

    # Guardar nueva posicion de los motores
    save_json(dict_motores)

def setup_motor_config(new_config: dict, motor_pines: dict, turn_counter: Pin):
    # Cargar JSON para despues poder guardar las nuevas posiciones
    d = load_json()

    for motor, ciclos in new_config.items():
        # Contador de ciclos
        count = 0

        # Prender el/los motor/es
        for pin in motor_pines[motor]:
            pin.value(1)

        # Contar vueltas hasta llegar a los ciclos necesarios
        while count < ciclos:
            if turn_counter.value() == 1:
                count += 1
            sleep_ms(100)

        # Apagar los motores
        for pin in motor_pines[motor]:
            pin.value(0)

    # Cambiar las posiciones actuales por las nuevas en el JSON
    d["Actuales"] = new_config

    # Re-escribir el JSON
    save_json(d)

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
