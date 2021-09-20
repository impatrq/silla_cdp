import ujson as json

class Usuario():
    instance_number = 1

    def __init__(self, nombre, dict_posicion):
        """
            Crear una instancia con `nombre`, asignarle su configuracion para la silla
            y guardar esa configuracion en el archivo `motor_data.json`.
        """
        self.nombre = nombre
        self.dict_posicion = dict_posicion

        self.add_config_to_json()

    def edit(self):
        pass
    
    def remove(self):
        pass

    def setup_config(self):
        pass

    def add_config_to_json(self):
        """
            Reescribir el archivo `motor_data.json` para agregar la configuracion de este usuario.
        """
        try:
            # Cargar json
            with open("motor_data.json", "r") as file:
                if not file.readline() == "":
                    d = json.load(file)
                else:
                    d = {}
            
            # Agregar posiciones de este usuario
            d[self.nombre] = self.dict_posicion
            d["Actuales"] = self.dict_posicion

            # Escribir en el json
            with open("motor_data.json", "w") as file:
                json.dump(d, file)
        except OSError:
            with open("motor_data.json", "w"):
                pass
            return self.add_config_to_json()

    def remove_config_from_json(self):
        pass

    def __repr__(self):
        return f"Usuario '{self.nombre}'.\nConfig:\n{self.dict_posicion}"
