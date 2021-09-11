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
        # Cargar json
        with open("motor_data.json", "r") as file:
            d = json.load(file)
        
        # Agregar posiciones de este usuario
        d[self.nombre] = self.dict_posicion
        d["Actuales"] = self.dict_posicion

        # Escribir en el json
        with open("motor_data.json", "w") as file:
            json.dump(d, file)

    def remove_config_from_json(self):
        pass