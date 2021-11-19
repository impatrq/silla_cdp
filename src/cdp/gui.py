import lvgl as lv
from cdp import uart, group
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

def users_cb(event):
    pass

def profile_cb(event, username, usericon):
    pass

def delete_user_cb(event, username):
    pass

def select_profile_cb(event, username):
    pass

def edit_profile_name_cb(event, username, usericon):
    pass

def delete_profile_cb(event, username, usericon):
    pass

# ===== FUNCIONES ===== #
def show_calib_instructions(which: str):
    print(which)

def update_sensor_state():
    pass

# ===== DIBUJAR PANTALLAS ===== #

def draw_edit_screen(scr, username, usericon):
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
    lv.btn.add_event_cb(btn, lambda e: select_profile_cb(e, username), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.OK + "  Seleccionar perfil")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 190)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, lambda e: edit_profile_name_cb(e, username, usericon), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.EDIT + "  Editar nombre")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 230)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, lambda e: users_cb(e), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.LEFT + "  Volver atras")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 270)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, lambda e: delete_profile_cb(e, username, usericon), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.TRASH + "  Borrar perfil")
    lv.group_t.add_obj(group, btn)

def draw_editname_screen(scr, username, usericon):
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
    lv.btn.add_event_cb(btn, lambda e: profile_cb(e, username, usericon), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text("Volver atras")

    kb = lv.keyboard(scr)
    kb.set_size(240, 320 // 2)
    kb.set_textarea(name_ta)

    group.add_obj(name_ta)
    group.add_obj(btn)
    group.add_obj(kb)

def draw_delete_screen(scr, username, usericon):
    h = lv.label(scr)
    h.set_pos(75, 16)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text(f"Borrar perfil\n\n{lv.SYMBOL.WARNING + '  ' + username + '  ' + lv.SYMBOL.WARNING}")

    h = lv.label(scr)
    h.set_pos(25, 80)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Esta accion es irreversible.\nConfirme su eleccion.")

    btn = lv.btn(scr)
    btn.set_pos(20, 140)
    lv.btn.add_event_cb(btn, lambda e: delete_user_cb(e, username), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text("Borrar")
    group.add_obj(btn)

    btn = lv.btn(scr)
    btn.set_pos(132, 140)
    lv.btn.add_event_cb(btn, lambda e: profile_cb(e, username, usericon), lv.EVENT.ALL, None)
    label = lv.label(btn)
    label.set_text("Cancelar")
    group.add_obj(btn)
