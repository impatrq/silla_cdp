import ujson as json
from cdp_helper import setup_motor_config

class Usuario():
    instance_number = 1

    def __init__(self, nombre, dict_posicion):
        """
            Crear una instancia con `nombre`, asignarle su configuracion para la silla
            y guardar esa configuracion en el archivo `motor_data.json`.
        """
        self.nombre = nombre
        self.dict_posicion = dict_posicion

        self.json_path = "settings/motor_data.json"

        self.add_config_to_json()

    def edit(self):
        pass
    
    def remove(self):
        pass

    def setup_config(self, motor_pines: dict, turn_counter):
        setup_motor_config(self.dict_posicion, motor_pines, turn_counter)

    def add_config_to_json(self):
        """
            Reescribir el archivo `motor_data.json` para agregar la configuracion de este usuario.
        """
        try:
            # Cargar json
            with open(self.json_path, "r") as file:
                try:
                    d = json.load(file)
                except:
                    d = {}
            
            # Agregar posiciones de este usuario
            d[self.nombre] = self.dict_posicion
            d["Actuales"] = self.dict_posicion

            # Escribir en el json
            with open(self.json_path, "w") as file:
                json.dump(d, file)
        except OSError:
            with open(self.json_path, "w"):
                pass
            return self.add_config_to_json()

    def remove_config_from_json(self):
        pass

    def __repr__(self):
        return f"Usuario '{self.nombre}'.\nConfig:\n{self.dict_posicion}"
