import PySimpleGUI as sg;
import cdp_main as main

def show_calib_instructions(which: str):
    print(which)

def update_sensor_state():
    pass

motorbool1 = False

motor_values = {
    "motor_cabezal" : False,
    "motor_ap" : False,
    "motor_lumbar" : False,
    "motor_assprof" : False,
    "motor_assheight" : False
}

bg_color = "#222222"
textStyle = {"size" : (40, 1), "text_color" : "#22dd22", "background_color" : bg_color}

layout = [
    [sg.Text(key = "txtMotorCabezal", **textStyle)],
    [sg.Text(key = "txtMotorAp", **textStyle)],
    [sg.Text(key = "txtMotorLumbar", **textStyle)],
    [sg.Text(key = "txtMotorAssProf", **textStyle)],
    [sg.Text(key = "txtMotorAssHeight", **textStyle)],
    [sg.Button("Decir hola", key = "btnTest"), sg.Button("Probar default", key = "btnDefault")]
]

def AbrirVentana():
    window = sg.Window(title = "Prueba", layout=layout, background_color=bg_color)

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WINDOW_CLOSED:
            break

        if event == "btnDefault":
            main.StartDefault()

        if event == "btnTest":
            main.Say("hola")

        window["txtMotorCabezal"].update("Motor Cabezal: " + str(motor_values["motor_cabezal"]))
        window["txtMotorAp"].update("Motor Apoyabrazos: " + str(motor_values["motor_ap"]))
        window["txtMotorLumbar"].update("Motor Lumbar: " + str(motor_values["motor_lumbar"]))
        window["txtMotorAssProf"].update("Motor Asiento Prof.: " + str(motor_values["motor_assprof"]))
        window["txtMotorAssHeight"].update("Motor Asiento Altura: " + str(motor_values["motor_assheight"]))

    window.close()