# Modulo con funciones auxiliares para silla CDP
import json
from machine import Pin
from utime import sleep_ms
from cdp import uart, sensor_us
from cdp.gui import draw_calib_screen

# ==================== SENSORES ==================== #

def sensor_check_range(which: str, minim: int = 0, maxim: int = 1023) -> bool:
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
    read = uart.send_and_receive(which)
    try:
        read = int(read)
        return maxim > read > minim
    except ValueError():
        print(read)
        return False

def sensor_check_all_states(sensors: list) -> bool:
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
        val = sensor_check_range(sensor[0], minim=sensor[1], maxim=sensor[2])
        i += int(val)

    return i >= well_sit_cond

def wait_for_interrupt_sensor(which: str):
    """
        Pregunta por el sensor `which` mediante 'comm', cuando recibe algo, sale del bucle.

        Args:
        `comm`: Objeto de `ControlUART` utilizado para el pedido.
        `which`: string de longitud 3 con el identificador del sensor.
    """
    while True:
        if sensor_check_range(which):
            break
        sleep_ms(100)

# ==================== ENCODER ==================== #

def set_select_encoder(value: str):
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
        r = uart.send_and_receive(f"mux{value}")
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
    with open("cdp/settings/motor_data.json", "r") as file:
        dict_motores = json.load(file)
    return dict_motores

# Funcion para guardar los datos de los motores
def save_json(data: dict):
    with open("cdp/settings/motor_data.json", "w") as outfile:
        json.dump(data, outfile)

# Mover motor hasta completar con el sensado requerido
def move_until_finished(turn_counter: Pin, motor_pines: list, sensors_to_check: list, mux_code:str, max_position: int) -> int:
    """
        Mueve un motor especifico y cuenta las vueltas hasta completar su sensado. Devuelve la nueva posicion.
    """
    # Safety checks
    for i in sensors_to_check:
        if len(i[1]) != 3:
            return 0
    if len(mux_code) != 3 or uart is None:
        return 0

    pos = 0
    sensor_type = sensors_to_check[0]

    # Setear encoder
    uart.send_bytes(f'mux{mux_code}')

    # Prender motores
    for pin in motor_pines:
        pin.value(1)

    # Actuar segun tipo de sensor asignado
    if sensor_type == "piezo":
        while True:
            pos += turn_counter.value()
            if any(sensor_check_range(sensor, minim, maxim) for sensor, minim, maxim in sensors_to_check[1:]) or pos >= max_position:
                break
    elif sensor_type == "ultra":
        # Safety check
        if sensor_us is None:
            return 0
        while True:
            pos += turn_counter.value()
            if sensor_us.send_pulse_centimeters() > 10 or pos >= max_position:
                break

    # Apagar motores
    for pin in motor_pines:
        pin.value(0)

    # Devolver nueva posicion
    return pos

def start_calibration(calibration_data: dict, turn_counter: Pin):
    """
        Realiza el proceso de calibración. Devuelve el diccionario de posiciones obtenido.

        Args:
        `comm`: Objeto de ControlUART para comunicacion con sensores.
        `sensor_us`: Objeto de Sensor_US para posicionamiento del cabezal.
        `calibration_data`: Diccionario con las configuraciones de calibración (sacados desde config).
        `turn_counter`: Pin donde entra la salida del multiplexor.
    """
    # Diccionario con nuevas posiciones
    new_pos = {}

    # Esperar por confirmacion de inicio
    draw_calib_screen('bar')
    #wait_for_interrupt_sensor('bar')
    sleep_ms(1000)

    # Formato config => [motor_pines[], sensors[type, str, min, max], mux_code, max_pos]
    for motor, config in calibration_data.items():
        print(f"Configurando {motor}")
        draw_calib_screen(motor)
        new_pos[motor] = 1 #move_until_finished(turn_counter, *config)
        sleep_ms(1000)

    # Devolver dict con posiciones
    return new_pos

def setup_motors_to_position(motor_pines: dict, turn_counter: Pin, new_config: dict = None):
    """
        Mueve los motores hasta la posicion indicada en `new_config`.

        - Para una posicion determinada, pasarle motor_pines['Adelante'] y una configuracion, previamente se debe estar en posicion cero.
        - Para volver a la posicion cero 'default', pasarle motor_pines['Atras'] y ninguna configuracion. Esto hace automaticamente que vuelva a la posicion cero.
    """
    # Para volver a posicion cero
    if new_config is None:
        new_config = {"assheight": 0, "assdepth": 0, "lumbar": 0,"cabezal": 0, "apbrazo": 0}

    # Cargar JSON para despues poder guardar las nuevas posiciones
    d = load_json()

    for motor, ciclos in new_config.items():
        # Contador de ciclos
        if ciclos == 0:
            count = -(d['Actuales'][motor])
        else:
            count = 0

        # Prender el/los motor/es
        for pin in motor_pines[motor]:
            pin.value(1)

        # Contar vueltas hasta llegar a los ciclos necesarios
        while count < ciclos:
            count += turn_counter.value()

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
