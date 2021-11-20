import ujson as json
from machine import Pin, time_pulse_us, UART
from utime import sleep_ms, sleep_us

# Necesario para evitar ImportError, parece?
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

class Usuario():
    json_motor_path = 'cdp/settings/motor_data.json'
    json_user_path = 'cdp/settings/user_data.json'

    def __init__(self, nombre, icon_path, dict_posicion):
        """
            Crear una instancia con `nombre`, asignarle su configuracion para la silla
            y guardar esa configuracion en los archivos JSON correspondientes.
        """
        self.nombre = nombre
        self.icon = icon_path
        self.dict_posicion = dict_posicion

        self.add_config_to_json()

    def edit(self, new_name = None, new_icon = None):
        if new_name is not None:
            try:
                with open(Usuario.json_motor_path, "r") as f:
                    d_m = json.load(f)
                with open(Usuario.json_user_path, "r") as f:
                    d_u = json.load(f)

                d_m[new_name] = self.dict_posicion
                del d_m[self.nombre]

                if new_icon is not None:
                    d_u[new_name] = new_icon
                    self.icon = new_icon
                else:
                    d_u[new_name] = self.icon
                del d_u[self.nombre]

                with open(Usuario.json_motor_path, "w") as f:
                    json.dump(d_m, f)
                with open(Usuario.json_user_path, "w") as f:
                    json.dump(d_u, f)

                self.nombre = new_name
                return True
            except ValueError:
                print("Error cambiando nombre e icono.")
                return False
        elif new_icon is not None:
            try:
                with open(Usuario.json_user_path, "r") as f:
                    d_u = json.load(f)

                d_u[self.nombre] = new_icon
                self.icon = new_icon

                with open(Usuario.json_user_path, "w") as f:
                    json.dump(d_u, f)
                return True
            except ValueError:
                print("Error cambiando icono.")
                return False
        return False

    @staticmethod
    def edit_from_file(username, new_name = None, new_icon = None):
        if new_name is not None:
            try:
                with open(Usuario.json_motor_path, "r") as f:
                    d_m = json.load(f)
                with open(Usuario.json_user_path, "r") as f:
                    d_u = json.load(f)

                d_m[new_name] = d_m[username]
                del d_m[username]

                if new_icon is not None:
                    d_u[new_name] = new_icon
                    del d_u[username]

                with open(Usuario.json_motor_path, "w") as f:
                    json.dump(d_m, f)
                with open(Usuario.json_user_path, "w") as f:
                    json.dump(d_u, f)

                return True
            except ValueError:
                print("Error cambiando nombre e icono.")
                return False
        elif new_icon is not None:
            try:
                with open(Usuario.json_user_path, "r") as f:
                    d_u = json.load(f)

                d_u[username] = new_icon

                with open(Usuario.json_user_path, "w") as f:
                    json.dump(d_u, f)
                return True
            except ValueError:
                print("Error cambiando icono.")
                return False
        return False

    def delete(self):
        # Eliminar configuracion de posicion
        self.remove_config_from_json(self.json_motor_path, self.nombre)

        # Eliminar configuracion de perfil
        self.remove_config_from_json(self.json_user_path, self.nombre)

    @staticmethod
    def delete_from_file(username):
        # Eliminar configuracion de posicion
        Usuario.remove_config_from_json(Usuario.json_motor_path, username)

        # Eliminar configuracion de perfil
        Usuario.remove_config_from_json(Usuario.json_user_path, username)

    def setup_config(self, motor_pines: dict, turn_counter):
        setup_motors_to_position(motor_pines, turn_counter, self.dict_posicion)

    def add_config_to_json(self):
        """
            Reescribir los archivos JSON para agregar la configuracion de este usuario.
        """
        # === Datos de motores === #
        self.rewrite_data_json(Usuario.json_motor_path, self.dict_posicion, "Actuales")

        # === Datos de perfil === #
        self.rewrite_data_json(Usuario.json_user_path, self.icon, "Actual")

    def rewrite_data_json(self, filepath, data_to_insert, place_to_insert):
        """
            Reescribir datos en un archivo JSON, si no existe crea el archivo y lo intenta de nuevo.

            Devuelve True si es exitoso.
        """
        try:
            with open(filepath, "r") as file:
                try:
                    d = json.load(file)
                except ValueError:
                    d = {}

            d[self.nombre] = data_to_insert
            d[place_to_insert] = data_to_insert

            with open(filepath, "w") as file:
                json.dump(d, file)
            return True
        except OSError:
            with open(filepath, "w"):
                pass
            return self.rewrite_data_json(filepath, data_to_insert, place_to_insert)

    @staticmethod
    def remove_config_from_json(where, which_key):
        with open(where, 'r') as f:
            d = json.load(f)

        del d[which_key]

        with open(where, 'w') as f:
            json.dump(d, f)

    def __repr__(self):
        return f"Usuario '{self.nombre}'.\nConfig:\n{self.dict_posicion}"

class Sensor_US:
    def __init__(self, trigger_pin: int, echo_pin: int, echo_timeout_us: int = 30000):
        """
            Clase especializada para la lectura del sensor ultrasonido.

            Args:
            `trigger_pin`: numero del pin de trigger.
            `echo_pin`: numero del pin de echo (debe estar protegido con resistencia de 1K).
            `echo_timeout_us`: timeout en microsegundos para la lectura del pulso.
        """
        self.__echo_timeout_us = echo_timeout_us

        self.__trigger = Pin(trigger_pin, Pin.OUT)
        self.__trigger.value(0)

        self.__echo = Pin(echo_pin, Pin.IN)

    def send_pulse_value(self):
        """
            Envia un pulso del `trigger` y luego lee la duracion del pulso del `echo` y la devuelve.
        """
        self.__trigger.value(0)
        sleep_us(5)
        self.__trigger.value(1)
        sleep_us(10)
        self.__trigger.value(0)

        try:
            pulse_time = time_pulse_us(self.__echo, 1, self.__echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range') from ex
            raise ex

    def send_pulse_centimeters(self):
        """
            Hace una lectura estandar del pulso de `echo` y usa la formula para convertir la lectura a centimetros.
        """
        lectura = self.send_pulse_value()
        return (lectura / 2) / 29.1

class StateMachine():
    def __init__(self, firstState: tuple = None):
        self.__executer = {}
        if firstState:
            self.__firstState = firstState[0]
            self.__state = firstState[0]

            self.__executer[firstState[0]] = firstState[1]

    @property
    def State(self):
        return self.__state

    @State.setter
    def State(self, state: int):
        self.__state = state

    @property
    def Executer(self):
        return self.__executer

    def change_first_state(self, new_state: tuple):
        try:
            del self.__executer[self.__firstState]
        except:
            print("No hay primer estado")
        self.__executer[new_state[0]] = new_state[1]
        self.__firstState = new_state[0]

    def add_state(self, state: tuple):
        self.__executer[state[0]] = state[1]

    def add_states(self, states: list):
        for tup in states:
            self.add_state(tup)

    def delete_state(self, state: int):
        del self.__executer[state]

    def delete_states(self, states: list):
        for state in states:
            self.delete_state(state)

    def start(self):
        self.__executer[self.__firstState]()
        self.next_state()

    def next_state(self):
        self.__executer[self.__state]()

class ControlUART():
    def __init__(self, baud:int, tx_pin: int, rx_pin: int):
        self.__uart = UART(2, baudrate=baud, tx=tx_pin, rx=rx_pin)
        print(f"Inicializado UART en los pines tx = {tx_pin}, rx = {rx_pin}")

    def send_bytes(self, msg: str):
        self.__uart.write(msg)

    def read_bytes(self) -> bytes:
        if self.__uart.any():
            r = self.__uart.read()
            return r
        return b'0'

    def read_string(self) -> str:
        rb = self.read_bytes()
        return rb.decode()

    def dummy_read(self, msg: str, times: int):
        i = 0
        while i < times:
            self.send_bytes(msg)
            sleep_ms(500)
            print(self.read_bytes())
            i += 1

    def send_and_receive(self, msg: str):
        self.send_bytes(msg)
        sleep_ms(500)
        return self.read_string()
