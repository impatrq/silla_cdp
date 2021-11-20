import lvgl as lv
import ujson as json
from cdp import fsm, group, scr, _users_list, motor_pines, turn_counter
from cdp.classes import Usuario
from utime import sleep, sleep_ms
import lodepng as png
from imagetools import get_png_info, open_png

def draw_calib_screen(which):
    group.remove_all_objs()

    lv.obj.clean(scr)

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

    s = lv.spinner(scr, 2000, 40)
    s.set_size(60, 60)
    s.set_pos(85, 200)

    lv.scr_load(scr)

from cdp.helper import setup_motors_to_position

# ===== CALLBACKS ===== #

def users_cb(event):
    draw_users_screen(_users_list)

def calibration_cb(event):
    fsm.State = 2 # CALIBRATING

def calib_name_cb(event, new_pos, kb):
    # Recibir posicion y nombre, guardarlo en el archivo
    username = kb.get_textarea().get_text()
    new_user = Usuario(username, '008-man.png', new_pos)
    _users_list.append(new_user)

    fsm.State = 3 # CALIBRATION_END

def profile_cb(event, username, usericon):
    draw_edit_screen(username, usericon)

def delete_user_cb(event, username):
    pass

def select_profile_cb(event, username, usericon):
    draw_profilewait_screen(username, usericon)

    for user in _users_list:
        if user.nombre == username:
            print(f"Configurando {username}")
            # setup_motors_to_position(motor_pines, turn_counter)

    fsm.State = 4

def edit_user_name_cb(event, username, usericon):
    draw_editname_screen(username, usericon)

def edit_profile_name_cb(event, username, usericon, kb):
    new_username = kb.get_textarea().get_text()
    draw_profilewait_screen(new_username, usericon)

    for user in _users_list:
        if user.nombre == username:
            user.edit(new_username)

    sleep(2)
    draw_edit_screen(new_username, usericon)

def delete_profile_cb(event, username, usericon):
    pass

# ===== DIBUJAR PANTALLAS ===== #

def draw_edit_screen(username, usericon):
    group.remove_all_objs()

    lv.obj.clean(scr)

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
    lv.btn.add_event_cb(btn, lambda e: select_profile_cb(e, username, usericon), lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.OK + "  Seleccionar perfil")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 190)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, lambda e: edit_user_name_cb(e, username, usericon), lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.EDIT + "  Editar nombre")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 230)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, users_cb, lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.LEFT + "  Volver atras")
    lv.group_t.add_obj(group, btn)

    btn = lv.btn(scr)
    btn.set_pos(16, 270)
    btn.set_width(200)
    lv.btn.add_event_cb(btn, lambda e: delete_profile_cb(e, username, usericon), lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.TRASH + "  Borrar perfil")
    lv.group_t.add_obj(group, btn)

    lv.scr_load(scr)

def draw_editname_screen(username, usericon):
    group.remove_all_objs()

    lv.obj.clean(scr)

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
    lv.btn.add_event_cb(btn, lambda e: profile_cb(e, username, usericon), lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text("Volver atras")

    kb = lv.keyboard(scr)
    kb.add_event_cb(lambda e: edit_profile_name_cb(e, username, usericon, kb), lv.EVENT.READY, None)
    kb.set_size(240, 320 // 2)
    kb.set_textarea(name_ta)

    group.add_obj(name_ta)
    group.add_obj(btn)
    group.add_obj(kb)

    lv.scr_load(scr)

def draw_delete_screen(username, usericon):
    group.remove_all_objs()

    lv.obj.clean(scr)

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

    lv.scr_load(scr)

def draw_profilewait_screen(username, usericon):
    lv.obj.clean(scr)

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

    lv.scr_load(scr)

def draw_users_screen(users):
    group.remove_all_objs()

    lv.obj.clean(scr)

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

    for user in users:
        btn = lv.btn(panel)
        btn.set_size(150, 150)
        btn.center()
        lv.btn.add_event_cb(btn, lambda e: profile_cb(e, user.nombre, user.icon), lv.EVENT.PRESSED, None)
        label = lv.label(btn)
        label.set_text(user.nombre)
        label.center()
        group.add_obj(btn)

    btn = lv.btn(panel)
    btn.set_size(150, 150)
    btn.center()
    lv.btn.add_event_cb(btn, lambda e: calibration_cb(e), lv.EVENT.PRESSED, None)
    label = lv.label(btn)
    label.set_text(lv.SYMBOL.PLUS)
    label.center()
    group.add_obj(btn)

    panel.update_snap(lv.ANIM.ON)
    lv.scr_load(scr)

def draw_calibname_screen(new_pos):
    group.remove_all_objs()

    lv.obj.clean(scr)

    h = lv.label(scr)
    h.set_pos(65, 16)
    h.set_text("Elegir nombre")

    name_ta = lv.textarea(scr)
    name_ta.set_placeholder_text("Nuevo perfil")
    name_ta.set_one_line(True)
    name_ta.set_pos(20, 45)
    name_ta.set_width(200)

    kb = lv.keyboard(scr)
    kb.add_event_cb(lambda e: calib_name_cb(e, new_pos, kb), lv.EVENT.READY, None)
    kb.set_size(240, 320 // 2)
    kb.set_textarea(name_ta)

    group.add_obj(name_ta)
    group.add_obj(kb)

    lv.scr_load(scr)

def draw_loading_screen():
    group.remove_all_objs()

    lv.obj.clean(scr)

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

    lv.scr_load(scr)
