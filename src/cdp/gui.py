import lvgl as lv
from cdp import uart, group
from utime import sleep_ms
import lodepng as png
from imagetools import get_png_info, open_png

# ===== CALLBACKS ===== #
def read_joystick_cb(drv, data):
    read = uart.send_and_receive("askswi").split('-')

    if read[0] > 954:
        print('Right')
        data.key = lv.KEY.RIGHT
        group.focus_next()
        sleep_ms(100)
    elif read[0] < 50:
        print('Left')
        data.key = lv.KEY.LEFT
        group.focus_prev()
        sleep_ms(100)
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

def select_profile_cb(event, username, usericon):
    pass

def edit_profile_name_cb(event, username, usericon):
    pass

def delete_profile_cb(event, username, usericon):
    pass

# ===== FUNCIONES ===== #
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

def draw_profilewait_screen(scr, username, usericon):
    h = lv.label(scr)
    h.set_pos(70, 16)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Configuracion")

    h = lv.label(scr)
    h.set_pos(25, 120)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Por favor, espere mientras\n se configura este perfil:")

    h = lv.label(scr)
    h.set_pos(145, 208)
    h.set_text(username)

    # Cargar imagen png
    with open(usericon, 'rb') as i:
        png_data = i.read()

    png_img_dsc = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data
    })

    img = lv.img(scr)
    img.set_pos(40, 200)
    img.set_zoom(256+256)
    raw_dsc = lv.img_dsc_t()
    get_png_info(None, png_img_dsc, raw_dsc.header)
    dsc = lv.img_decoder_dsc_t({'src': png_img_dsc})
    if open_png(None, dsc) == lv.RES.OK:
        raw_dsc.data = dsc.img_data
        raw_dsc.data_size = raw_dsc.header.w * raw_dsc.header.h * lv.color_t.__SIZE__
        img.set_src(raw_dsc)

def draw_users_screen(scr, users):
    h = lv.label(scr)
    h.set_pos(90, 15)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Usuarios")

    h = lv.label(scr)
    h.set_pos(64, 75)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Seleccione uno")

    panel = lv.obj(scr)
    panel.set_pos(10, 100)
    panel.set_size(220, 190)
    panel.set_scroll_snap_x(lv.SCROLL_SNAP.CENTER)
    panel.set_flex_flow(lv.FLEX_FLOW.ROW)

    for i, user in enumerate(users):
        btn = lv.btn(panel)
        btn.set_size(150, 150)
        btn.center()
        lv.btn.add_event_cb(btn, lambda e: profile_cb(e, None, None))
        label = lv.label(btn)
        label.set_text(user)
        label.center()
        group.add_obj(btn)

    panel.update_snap(lv.ANIM.ON)

def draw_calib_screen(scr, which):
    h = lv.label(scr)
    h.set_pos(75,16)
    h.set_text("Calibrando...")

    i = lv.label(scr)
    i.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

    if which == 'bar':
        i.set_pos(40, 120)
        i.set_text("Instrucciones de barra")
    elif which == 'assheight':
        i.set_pos(55, 120)
        i.set_text("Instrucciones de \naltura de asiento")
    elif which == 'assdepth':
        i.set_pos(35, 120)
        i.set_text("Instrucciones de \nprofundidad de asiento")
    elif which == 'lumbar':
        i.set_pos(30, 120)
        i.set_text("Instrucciones de lumbar")
    elif which == 'cabezal':
        i.set_pos(30, 120)
        i.set_text("Instrucciones de cabezal")
    elif which == 'apbrazo':
        i.set_pos(10, 120)
        i.set_text("Instrucciones de apoyabrazos")

def draw_calibname_screen(scr):
    h = lv.label(scr)
    h.set_pos(65, 16)
    h.set_text("Elegir nombre")

    name_ta = lv.textarea(scr)
    name_ta.set_placeholder_text("Nuevo perfil")
    name_ta.set_one_line(True)
    name_ta.set_pos(20, 45)
    name_ta.set_width(200)

    kb = lv.keyboard(scr)
    kb.set_size(240, 320 // 2)
    kb.set_textarea(name_ta)

    g.add_obj(name_ta)
    g.add_obj(btn)
    g.add_obj(kb)

def draw_calibname_screen():
    h = lv.label(scr)
    h.set_pos(95, 16)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("C.D.P.")

    s = lv.spinner(scr, 1000, 60)
    s.set_size(100, 100)
    s.center()

    h = lv.label(scr)
    h.set_pos(85, 220)
    h.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    h.set_text("Cargando...")
