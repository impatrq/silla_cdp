import lvgl as lv
from cdp import uart, scr, group
import lodepng as png
from imagetools import get_png_info, open_png

# ===== CALLBACKS ===== #
def read_joystick_cb(drv, data):
    read = uart.send_and_receive("askswi").split('-')

    if read[0] > 954:
        print('Right')
        data.key = lv.KEY.RIGHT
    elif read[0] < 50:
        print('Left')
        data.key = lv.KEY.LEFT
    else:
        data.key = 0

    if read[2] == 0:
        print('Pressed')
        data.key = lv.KEY.ENTER
        data.state = lv.INDEV_STATE.PRESSED
    else:
        data.key = 0
        data.state = lv.INDEV_STATE.RELEASED

    return False

def profile_cb(drv, data):
    pass

def select_profile_cb(drv, data):
    pass

def edit_profile_name_cb(drv, data):
    pass

def edit_profile_icon_cb(drv, data):
    pass

def delete_profile_cb(drv, data):
    pass

# ===== FUNCIONES ===== #
def show_calib_instructions(which: str):
    print(which)

def update_sensor_state():
    pass

# ===== DIBUJAR PANTALLAS ===== #

def draw_edit_screen(username, usericon):
    h1 = lv.label(scr)
    h1.set_pos(96, 16)
    h1.set_text("Perfil")

    h1 = lv.label(scr)
    h1.set_pos(145, 80)
    h1.set_text(username)

    # Cargar imagen png
    with open(usericon, 'rb') as i:
        png_data = i.read()

    png_img_dsc = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data
    })

    img = lv.img(scr)
    img.set_pos(40, 72)
    img.set_zoom(256+256)
    raw_dsc = lv.img_dsc_t()
    get_png_info(None, png_img_dsc, raw_dsc.header)
    dsc = lv.img_decoder_dsc_t({'src': png_img_dsc})
    if open_png(None, dsc) == lv.RES.OK:
        raw_dsc.data = dsc.img_data
        raw_dsc.data_size = raw_dsc.header.w * raw_dsc.header.h * lv.color_t.__SIZE__
        img.set_src(raw_dsc)

    # Agregar botones
    btn = lv.btn(scr)
    btn.set_pos(16, 150)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, select_profile_cb, lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.OK + "  Seleccionar perfil")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 190)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, edit_profile_name_cb, lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.EDIT + "  Editar nombre")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 230)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, edit_profile_icon_cb, lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.EDIT + "  Editar icono")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 270)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, delete_profile_cb, lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.TRASH + "  Borrar perfil")
    lv.group_t.add_obj(group, btn)

def draw_editname_screen():
    h = lv.label(scr)
    h.set_pos(65, 16)
    h.set_text("Editar nombre")

    name_ta = lv.textarea(scr)
    name_ta.set_placeholder_text("Nuevo nombre")
    name_ta.set_one_line(True)
    name_ta.set_pos(20, 45)
    name_ta.set_width(200)

    btn = lv.btn(scr)
    btn.set_pos(65, 110)
    lv.btn.add_event_cb(btn, profile_cb, lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text("Volver atras")

    kb = lv.keyboard(scr)
    kb.set_size(240, 320 // 2)
    kb.set_textarea(name_ta)

    group.add_obj(name_ta)
    group.add_obj(btn)
    group.add_obj(kb)
