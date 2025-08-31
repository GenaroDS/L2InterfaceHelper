import easyocr
from pystray import Menu, MenuItem, Icon
from PIL import Image as PILImage
import numpy as np
from PIL import ImageGrab
import time
import tkinter as tk
import threading
import ctypes
import torch, torchvision
import difflib 
from tkinter import font
from PIL import Image, ImageTk
import os
import msvcrt
import sys
import ctypes
from ctypes import wintypes

 # El problema es ccuando pasan 30 segundos?

global root  # declarar root global
reader = None  # init perezosa

tray_icon = None
stop_event = threading.Event()
visible_event = threading.Event()  # controla si el OCR corre
visible_event.set()   
_kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
CreateMutexW  = _kernel32.CreateMutexW
CreateMutexW.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR)
CreateMutexW.restype  = wintypes.HANDLE
CloseHandle   = _kernel32.CloseHandle
CloseHandle.argtypes  = (wintypes.HANDLE,)
CloseHandle.restype   = wintypes.BOOL

ERROR_ALREADY_EXISTS = 183

mutex_handle = None  # global

iconos = {}
# --- Hablidades ----
ultimates_data = [
    {"nombre": "Shield of Faith", "duracion": 30, "cd": 900},
    {"nombre": "Seed of Revenge", "duracion": 15, "cd": 900},    

    
    {"nombre": "Bear Spirit Totem", "duracion": 300, "cd": 30},


    {"nombre": "Hawk Spirit Totem", "duracion": 300, "cd": 30},


    {"nombre": "Rabbit Spirit Totem", "duracion": 300, "cd": 30},


    {"nombre": "Ogre Spirit Totem", "duracion": 300, "cd": 30},


    {"nombre": "Item Skill Might", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Shield", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Magic Barrier", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Duel Might", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Lesser Celestial Shield", "duracion": 10, "cd": 300},
    {"nombre": "Item Skill Wild Magic", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Music refresh", "duracion": 120, "cd": 300},
    {"nombre": "Item Skill Vampiric Rage", "duracion": 120, "cd": 300},
    {"nombre": "Arcane Shield", "duracion": 10, "cd": 120},  
    {"nombre": "Spirit of Phoenix", "duracion": 15, "cd": 900},
    {"nombre": "Mystic Immunity", "duracion": 30, "cd": 900},
    {"nombre": "Evas Will", "duracion": 15, "cd": 900},
    {"nombre": "Pain of Shillen", "duracion": 15, "cd": 900},
    {"nombre": "Vengeance", "duracion": 30, "cd": 900},
    {"nombre": "Ultimate Defense", "duracion": 30, "cd": 900},
    {"nombre": "Angelic Icon", "duracion": 60, "cd": 300},
    {"nombre": "Flame Icon", "duracion": 60, "cd": 900},
    {"nombre": "Touch of Life", "duracion": 120, "cd": 300},
    {"nombre": "Templars Frenzy", "duracion": 60, "cd": 300},
    {"nombre": "Spirit of Shillen", "duracion": 60, "cd": 300},
    {"nombre": "Wind Riding", "duracion": 30, "cd": 900},
    {"nombre": "Ghost Walking", "duracion": 30, "cd": 900},
    {"nombre": "Exciting Adventure", "duracion": 30, "cd": 900},
    {"nombre": "Ultimate Evasion", "duracion": 59, "cd": 900},
    {"nombre": "Hide", "duracion": 30, "cd": 200},
    {"nombre": "Dodge", "duracion": 10, "cd": 60},
    {"nombre": "Counterattack", "duracion": 10, "cd": 70},
    {"nombre": "Battle Rhapsody", "duracion": 30, "cd": 240},
    {"nombre": "Song of Protection", "duracion": 30, "cd": 240},
    {"nombre": "Servitor Empowerment", "duracion": 30, "cd": 900},
    {"nombre": "Summon Barrier", "duracion": 30, "cd": 300},
    {"nombre": "Seven Arrow", "duracion": 0, "cd": 180},
    {"nombre": "Blessing of Eva", "duracion": 0, "cd": 600},
    {"nombre": "Brillant Purge", "duracion": 0, "cd": 60},
    {"nombre": "Turn to Stone", "duracion": 8, "cd": 300},
    {"nombre": "Enlightenment", "duracion": 20, "cd": 600},
    {"nombre": "Celestial Shield", "duracion": 10, "cd": 900},
    {"nombre": "Celestial Aegis", "duracion": 10, "cd": 900},
    {"nombre": "Final Secret", "duracion": 30, "cd": 120},
    {"nombre": "Battle Cry", "duracion": 0, "cd": 120},
    {"nombre": "Sonic Barrier", "duracion": 10, "cd": 900},
    {"nombre": "Maximum Energy", "duracion": 0, "cd": 60},
    {"nombre": "Maximum Sonic Focus", "duracion": 0, "cd": 75},
    {"nombre": "Force Barrier", "duracion": 10, "cd": 900},
    {"nombre": "Second Wind", "duracion": 0, "cd": 120},
    {"nombre": "Maximum Force Focus", "duracion": 0, "cd": 75},
    {"nombre": "Revival", "duracion": 0, "cd": 900},
    {"nombre": "Battle Roar", "duracion": 0, "cd": 60},
    {"nombre": "Braveheart", "duracion": 0, "cd": 120},
    {"nombre": "Frenzy", "duracion": 90, "cd": 180},
    {"nombre": "Guts", "duracion": 90, "cd": 300},
    {"nombre": "Star Fall", "duracion": 10, "cd": 300},
    {"nombre": "Meteor", "duracion": 10, "cd": 300},
    {"nombre": "Body Reconstruction", "duracion": 0, "cd": 300},
    {"nombre": "Eye for eye", "duracion": 10, "cd": 70},
    {"nombre": "Painkiller", "duracion": 8, "cd": 300},
    {"nombre": "Ultimate Escape", "duracion": 20, "cd": 300},
    {"nombre": "Soul Roar", "duracion": 0, "cd": 210},
    {"nombre": "Sword Shield", "duracion": 30, "cd": 350},
    {"nombre": "Soul Barrier", "duracion": 50, "cd":60},
    {"nombre": "Red Talisman of Maximum Clarity", "duracion": 90, "cd":600},
    {"nombre": "Blue Talisman of Divine Protection", "duracion": 9, "cd":600}
]

grupos_exclusivos = {
    "totems": [
        "hawk spirit totem",
        "bear spirit totem",
        "rabbit spirit totem",
        "ogre spirit totem"
    ]
}

# --- Configuración global ---
rect_width = 215
rect_height = 50
solapa_height = 11
ultimates_dict = {entry['nombre'].lower(): entry for entry in ultimates_data}
pos = {'x': 0, 'y': 0, 'width': rect_width, 'height': rect_height}
active_alerts = {}

# --- Inicialización de OCR ---
reader = easyocr.Reader(['en'], gpu=True)

def resource_path(rel):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)

# --- Carga de íconos ---
def cargar_iconos():
    if not tk._default_root:
        root = tk.Tk()
        root.withdraw()

    ruta_iconos = ruta_iconos = resource_path("Icons")
    total = len(ultimates_dict)
    cargados = 0
    faltantes = []

    if not os.path.exists(ruta_iconos):
        raise FileNotFoundError(f"No se encontró la carpeta de íconos: {ruta_iconos}")

    archivos_disponibles = {f.lower(): f for f in os.listdir(ruta_iconos) if f.endswith(".png")}

    for nombre in ultimates_dict.keys():
        posibles_nombres = [
            nombre.replace("'", "").lower() + ".png",
            nombre.replace("'", "").replace(" ", "_").lower() + ".png",
            nombre.replace("'", "").replace(" ", "").lower() + ".png"
        ]

        match = next((archivos_disponibles[f] for f in posibles_nombres if f in archivos_disponibles), None)
        if match:
            path = os.path.join(ruta_iconos, match)
            imagen = Image.open(path).resize((32, 32), Image.Resampling.LANCZOS)
            iconos[nombre] = imagen.copy()  # solo PIL.Image

            cargados += 1
        else:
            faltantes.append(nombre)

    print(f"[Iconos] {cargados} de {total} íconos cargados correctamente.")
    if faltantes:
        print("[Faltantes] No se encontraron íconos para las siguientes habilidades:")
        for nombre in faltantes:
            print("  -", nombre)



def obtener_posicion_centrada():
    """Calcula la posición X centrada en la pantalla"""
    user32 = ctypes.windll.user32
    sw = user32.GetSystemMetrics(0)
    pos['x'] = (sw - rect_width) // 2
    pos['y'] = 50

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=True)  # poné gpu=False para testear arranque
    return reader

def crear_overlay():
    global root, frame_iconos
    obtener_posicion_centrada()

    margin_left = 140  # espacio reservado para el label "READY"
    visible_h = rect_height + solapa_height
    canvas_h = int(visible_h * 2.5)
    total_width = rect_width + 200 + margin_left

    root = tk.Tk()
    tk._default_root = root
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "white")
    root.configure(bg='white')
    root.geometry(f"{total_width}x{canvas_h}+{pos['x']}+{pos['y']}")

    hide_window() 

    canvas = tk.Canvas(
    root,
    width=total_width,
    height=visible_h,
    bg='white',                # Color de fondo visible1
    highlightthickness=0,          # Grosor del borde
    highlightbackground='red'      # Color del borde visible
)
    
    canvas.pack()

    # Dibujar rectángulo desplazado a la derecha
    canvas.create_rectangle(margin_left-2, 0, margin_left + rect_width + 1, solapa_height, fill='#427ed7', outline='#427ed7')
    canvas.create_rectangle(margin_left, solapa_height, margin_left + rect_width, visible_h, outline='#427ed7', width=4)

    # Label fijo a la izquierda
        # Botón RESET a la izquierda
    boton_reset = tk.Button(
        root,
        text="RESET",
        command=reset_alertas,
        bg='#427ed7',
        fg="#D1D1D1",
        font=('Segoe UI', 6, 'bold'),
        relief='flat',
        cursor='hand2'
    )
    boton_reset.place(x=138, y=solapa_height-34 + (rect_height) // 2, width=30, height=11)

    boton_cerrar = tk.Button(
        root,
        text="❌",
        command=lambda: hide_window(),
        bg='#427ed7',
        activebackground='#427ed7',
        fg="#D1D1D1",
        font=('Segoe UI', 7, 'bold'),
        relief='flat',
        cursor='hand2'
    )
    boton_cerrar.place(x=total_width - 220, y=0, width=20, height=solapa_height)

    # Frame de íconos debajo del rectángulo, también desplazado
    frame_iconos = tk.Frame(root, bg='white')
    frame_iconos.place(x=margin_left, y=visible_h + 4)

    def on_press(e):
        canvas.grab_data = {'x': e.x_root, 'y': e.y_root, 'orig_x': pos['x'], 'orig_y': pos['y']}

    def on_drag(e):
        gd = canvas.grab_data
        dx, dy = e.x_root - gd['x'], e.y_root - gd['y']
        pos['x'] = gd['orig_x'] + dx
        pos['y'] = gd['orig_y'] + dy
        root.geometry(f"{total_width}x{canvas_h}+{pos['x']}+{pos['y']}")
        actualizar_posiciones_labels()

    canvas.tag_bind("all", "<ButtonPress-1>", on_press)
    canvas.tag_bind("all", "<B1-Motion>", on_drag)

    root.canvas = canvas
    root.protocol("WM_DELETE_WINDOW", hide_window)
    root.mainloop()



def iniciar_overlay():
    """Ejecuta el overlay en un hilo separado"""
    threading.Thread(target=crear_overlay, daemon=True).start()

def capturar_imagen():
    """Captura la imagen dentro del rectángulo actual"""
    margin_left = 140  # debe coincidir con el usado en crear_overlay
    bbox = (
        pos['x'] + margin_left,
        pos['y'] + solapa_height,
        pos['x'] + margin_left + rect_width,
        pos['y'] + solapa_height + rect_height
    )
    return np.array(ImageGrab.grab(bbox=bbox))


def detectar_habilidades(imagen):
    resultados = get_reader().readtext(imagen, detail=0)
    now = time.time()

    for texto in resultados:
        print(f"[OCR]: {texto}")    
        txt = texto.strip().lower()
        match = difflib.get_close_matches(txt, list(ultimates_dict.keys()), n=1, cutoff=0.75)
        if match:
            habilidad = match[0]
            if habilidad in active_alerts and active_alerts[habilidad].get("ready", False):
                data = active_alerts[habilidad]
                if data.get('label_ready'):
                    data['label_ready'].destroy()
                active_alerts.pop(habilidad)

            if habilidad not in active_alerts:
                duracion = ultimates_dict[habilidad]['duracion']
                root.after(0, registrar_alerta, habilidad, now, duracion)



def registrar_alerta(habilidad, now, duracion):


    global root, frame_iconos
    
    for grupo, miembros in grupos_exclusivos.items():
        if habilidad in miembros:  # si el skill pertenece a este grupo
            for otro in list(active_alerts.keys()):
                if otro != habilidad and otro in miembros:
                    # borrar solo lo visual (duración / ícono), NO el CD
                    data_otro = active_alerts[otro]
                    if data_otro.get('container'):
                        data_otro['container'].destroy()
                        data_otro['container'] = None
                    # mantener label_cd y cd_end para que siga contando cooldown
                    # marcar como expirado visualmente
                    data_otro['end'] = now  # fuerza expiración del timer
                    print(f"[EXCLUSIVO] {otro.title()} reemplazado por {habilidad.title()}")

    margin_left = 140  # mantener coherencia con crear_overlay
    base_x = rect_width + margin_left
    base_y = 0
    y_offset = len(active_alerts) * 18

    cd = ultimates_dict[habilidad]['cd']
    mostrar_cd = True
    cd_end = now + cd if mostrar_cd else None
    
    label_cd = None
    label_ready = None
    if mostrar_cd:
        label_cd = tk.Label(
            root,
            text=f"{habilidad.title()} CD: {cd}",
            bg='#427ed7',
            fg='#f0f0f0',
            font=('Segoe UI', 9),
            padx=3,
            pady=0,
            anchor='w',
            justify='left'
        )
        label_cd.place(x=base_x, y=base_y + y_offset)

    icono = iconos.get(habilidad)
    canvas = None
    texto_id = None
    contenedor = None

    if icono:
        photo = ImageTk.PhotoImage(icono)
        contenedor = tk.Frame(frame_iconos, bg='white', width=32, height=32)
        contenedor.pack_propagate(False)
        contenedor.pack(side='left', padx=2)

        canvas = tk.Canvas(contenedor, width=32, height=32, bg='white', highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.image = photo  # evitar GC

        x, y = 16, 16
        texto = str(duracion)
        borde_id = canvas.create_text(x, y, text=texto, fill='black', font=('Segoe UI', 14, 'bold'))
        texto_id = canvas.create_text(x, y, text=texto, fill='#f3f3f3', font=('Segoe UI', 13, 'bold'))

    active_alerts[habilidad] = {
        'canvas': canvas,
        'texto_id': texto_id,
        'borde_id': borde_id,
        'container': contenedor,
        'end': now + duracion,
        'cd': cd,
        'cd_end': cd_end,
        'mostrar_cd': mostrar_cd,
        'y_offset': y_offset,
        'ready': False,
        'label_cd': label_cd,
        'label_ready': None,
    }


def actualizar_alertas():
    now = time.time()
    expiradas = []

    for key in list(active_alerts):
        data = active_alerts[key]

        # Protección contra dicts incompletos
        if 'end' not in data or 'cd' not in data:
            continue

        restante = int(data['end'] - now)
        mostrar_cd = data.get('mostrar_cd', False)
        cd_restante = int(data['cd_end'] - now) if data.get('cd_end') else None
        cd_restante = max(cd_restante, 0) if cd_restante is not None else None

        # Actualizar countdown del overlay (duración)
        if restante > 0:
            if data.get('canvas') and data.get('texto_id'):
                data['canvas'].itemconfigure(data['texto_id'], text=str(restante))
            if data.get('borde_id'):
                data['canvas'].itemconfigure(data['borde_id'], text=str(restante))
        else:
            if data.get('container'):
                data['container'].destroy()
                data['container'] = None

        # Si no tiene CD que contar y ya expiró, eliminar
        if not mostrar_cd and not data.get('ready', False):
            expiradas.append(key)

        # Procesar cooldown
        if mostrar_cd:
            if cd_restante > 0:
                if data.get('label_cd'):
                    texto = f"{key.title()} CD: {cd_restante}"
                    data['label_cd'].configure(text=texto)
            else:
                # CD finalizado → mostrar READY si no se había hecho
                if not data.get('ready', False):
                    if data.get('label_cd'):
                        data['label_cd'].destroy()
                        data['label_cd'] = None

                    print("[READY] Habilidad lista:", key)

                    if not data.get('label_ready'):
                        label_ready = tk.Label(
                            root,
                            text=f"{key.title()}: ✅",
                            bg='#427ed7',
                            fg='#f0f0f0',
                            font=('Segoe UI', 9),
                            padx=3,
                            pady=0,
                            anchor='e',         # ← alinear a la derecha del label
                            justify='right'
                        )
                        data['label_ready'] = label_ready
                        data['ready_time'] = time.time()
                        data['ready'] = True
                        print(f"[DEBUG] {key.title()} cambió a estado READY")
                        #label_ready.place(x=10, y=2 + y_offset)

                    # Marcar para eliminación lógica (pero no visual)
                    expiradas.append(key)

    # Eliminar entradas expiradas (READY o sin CD)
    for key in expiradas:
        data = active_alerts[key]
        if not data.get('ready', False):
            # Si no está en estado READY, eliminar completamente
            if data.get('label_cd'):
                data['label_cd'].destroy()
            if data.get('container'):
                data['container'].destroy()
            active_alerts.pop(key)

    # Reposicionar etiquetas visuales (CD y READY)
    actualizar_posiciones_labels()





def actualizar_posiciones_labels():
    margin_left = 140
    base_x = rect_width + margin_left
    base_y = 0

    # 1. Apilar etiquetas CD a la derecha
    cd_labels = [d for d in active_alerts.values() if d.get('label_cd')]
    for idx, data in enumerate(cd_labels):
        y_offset = idx * 18
        data['y_offset'] = y_offset
        data['label_cd'].place(x=base_x, y=base_y + y_offset)

    # 2. Apilar etiquetas READY a la izquierda
    ready_labels = [d for d in active_alerts.values() if d.get('label_ready')]
    for idx, data in enumerate(ready_labels):
        y_offset = idx * 18
        max_width = margin_left - 10
        data['y_offset'] = y_offset
        data['label_ready'].place(x=margin_left - data['label_ready'].winfo_reqwidth(), y=0 + y_offset)

def reset_alertas():
    global active_alerts
    for key, data in active_alerts.items():
        if data.get('label_cd'):
            data['label_cd'].destroy()
        if data.get('label_ready'):
            data['label_ready'].destroy()
        if data.get('container'):
            data['container'].destroy()
    active_alerts.clear()
    actualizar_posiciones_labels()
    print("[RESET] Estado reiniciado")




def bucle_principal():
    while not stop_event.is_set():
        if not visible_event.wait(timeout=0.5):
            continue
        if stop_event.is_set():
            break
        imagen = capturar_imagen()
        detectar_habilidades(imagen)
        actualizar_alertas()
        time.sleep(0.15)

# --- Inicio del sistema ---

def check_single_instance_mutex(name=r"Local\SkillOCR_Singleton"):
    """
    Devuelve el handle del mutex si es la primera instancia.
    Si ya existe otra, termina el proceso.
    """
    h = CreateMutexW(None, False, name)
    if not h:
        raise ctypes.WinError(ctypes.get_last_error())
    # Si el mutex ya existía, GetLastError == ERROR_ALREADY_EXISTS
    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        print("[ERROR] Ya hay una instancia en ejecución.")
        sys.exit(0)
    return h

def get_icon_path(icon_name):
    return resource_path(os.path.join('Icons', icon_name))

def tray_set_icon(name):
    global tray_icon
    if tray_icon is not None:
        try:
            tray_icon.icon = PILImage.open(get_icon_path(name))
        except Exception:
            pass

def show_window():
    if root and root.winfo_exists():
        root.deiconify()
        root.lift()
        root.attributes("-topmost", True)
        visible_event.set()  # reanudar OCR

def hide_window():
    if root and root.winfo_exists():
        root.withdraw()
    visible_event.clear()  

def exit_app():
    visible_event.set()
    stop_event.set()
    try:
        if tray_icon:
            tray_icon.stop()
    except Exception:
        pass
    global mutex_handle
    if mutex_handle:
        CloseHandle(mutex_handle)
        mutex_handle = None
    if root and root.winfo_exists():
        root.after(0, root.destroy)
    os._exit(0)

def setup_tray():
    global tray_icon
    menu = Menu(
        MenuItem('Show', lambda i: show_window()),
        MenuItem('Hide', lambda i: hide_window()),
        MenuItem('Exit',     lambda i: exit_app())
    )
    try:
        img = PILImage.open(get_icon_path('Systray.png'))  # 16–32 px recomendado
    except Exception as e:
        print('[TRAY] Icono no cargado, fallback:', e)
        from PIL import Image as _PILImg
        img = _PILImg.new('RGBA', (16, 16), (0, 0, 0, 255))

    tray_icon = Icon('SkillOCR', img, 'L2 Interface Helper', menu=menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()


# (opcional) si querés cambiar solo el tooltip:
def tray_set_tooltip(texto):
    if tray_icon:
        tray_icon.title = texto

if __name__ == "__main__":
    mutex_handle = check_single_instance_mutex()  # <- sin archivo en disco
    # print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CUDA no disponible")

    cargar_iconos()

    # Iniciar icono de bandeja (hilo propio)
    setup_tray()

    # Iniciar OCR en background
    threading.Thread(target=bucle_principal, daemon=True).start()

    # Iniciar UI en hilo principal
    crear_overlay()
