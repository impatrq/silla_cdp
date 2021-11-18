import lvgl as lv
from cdp import uart

# ===== CALLBACKS ===== #
def read_joystick_cb(drv, data):
    read = uart.send_and_receive("askswi").split('-')

    if read[0] > 900:
        print('Right')
        data.key = lv.KEY.RIGHT
    elif read[0] < 100:
        print('Left')
        data.key = lv.KEY.LEFT
    else:
        data.key = 0

    if read[2] == 0:
        print('Pressed')
        data.state = lv.INDEV_STATE.PRESSED
    else:
        data.state = lv.INDEV_STATE.RELEASED

    return False

# ===== FUNCIONES ===== #
def show_calib_instructions(which: str):
    print(which)

def update_sensor_state():
    pass
