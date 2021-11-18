from cdp import _global_config, STARTING, IDLE
from cdp.classes import StateMachine

def wait_for_action():
    # TODO: interacción con la GUI
    print(".")
    fsm.next_state()

def main():
    if _global_config["first_time_open"]:
        # TODO: Bienvenida por la GUI + primera calibracion
        print("Bienvenido a Silla CDP")
        _global_config["first_time_open"] = False
    # TODO: Carga de pantalla inicial por la GUI
    print("Pantalla de usuarios")

    # Cambiar de estado a espera
    fsm.State = IDLE

# Instancia de la FSM
fsm = StateMachine((STARTING, main))

if __name__ == "__main__":
    # Agregar estados a la FSM
    fsm.add_states([
        (IDLE, wait_for_action)
    ])

    # Arrancar la FSM
    fsm.start()
