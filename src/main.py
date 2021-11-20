from cdp import _global_config, _users_list, fsm, turn_counter, motor_pines
from cdp.gui import draw_loading_screen, draw_users_screen, draw_calibname_screen
from cdp.helper import start_calibration, setup_motors_to_position
from utime import sleep

# ===== FSM STATES ===== #
STARTING, IDLE, CALIBRATING, CALIBRATION_END, USER_SCREEN = range(5)

def wait_for_action():
    while True:
        print("Waiting...")
        sleep(1)
        if fsm.State != IDLE:
            break
    fsm.next_state()

def do_calibration():
    print("Start calibration")
    #setup_motors_to_position(motor_pines['Atras'], turn_counter, None)
    new_pos = start_calibration(_global_config['calibration_data'], turn_counter)
    draw_calibname_screen(new_pos)

    fsm.State = IDLE
    fsm.next_state()

def finish_calibration():
    print("Finish calibration")
    draw_loading_screen()
    sleep(1)
    draw_users_screen(_users_list)

    fsm.State = IDLE
    fsm.next_state()

def main():
    draw_loading_screen()
    sleep(3)
    draw_users_screen(_users_list)

    # Cambiar de estado a espera
    fsm.State = IDLE

if __name__ == "__main__":
    fsm.change_first_state((STARTING, main))

    # Agregar estados a la FSM
    fsm.add_states([
        (IDLE, wait_for_action),
        (CALIBRATING, do_calibration),
        (CALIBRATION_END, finish_calibration)
    ])

    # Arrancar la FSM
    fsm.start()
