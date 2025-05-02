import os, sys, json, subprocess, pystray
from pynput import keyboard
from ui import mk_config_dir, get_config_dir, get_text_from_key, run
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from PIL import Image

mk_config_dir()

def log(*args):
    print(" ".join([str(x) for x in list(args)]))
    with open(os.path.join(get_config_dir(),"latest.log"),"a") as f:
        f.write("\n")
        for x in list(args):
            f.write(" "+str(x))

CDIR = os.path.abspath("./") if not hasattr(sys,"_MEIPASS") else sys._MEIPASS
log(f"CDIR={CDIR}")

class FileChangedHandler(FileSystemEventHandler):
    def __init__(self, path:str):
        super().__init__()
        self.path = path
    
    def on_modified(self, event):
        if event.src_path.endswith(self.path):
            update_shortcuts()

def f_upd_t():
    handler = FileChangedHandler("config.json")
    observer = Observer()
    observer.schedule(handler,get_config_dir(),recursive=False)
    observer.start()

watch_thread = Thread(target=f_upd_t)
watch_thread.start()

pressed = {}

MAP = { # Qt => pynput
    "Meta": "cmd",
    "Control": "ctrl",
    "CapsLock": "caps_lock"
}

def map_from_qt_key(key:str): # `key` is `str` from `Qt.Key`
    if key in MAP.keys():
        return MAP[key]
    return key.lower()

SHORTCUTS = []

def update_shortcuts():
    global SHORTCUTS
    with open(os.path.join(get_config_dir(),"config.json")) as f:
        SHORTCUTS = json.load(f)
        log("SHORTCUTS => ",SHORTCUTS)

update_shortcuts()

def on_press(key):
    log(f"Pressed: {get_text_from_key(key)}")
    if get_text_from_key(key) in pressed and pressed[get_text_from_key(key)]: return
    pressed[get_text_from_key(key)] = True
    for s in SHORTCUTS:
        cut:str = s["Shortcut"]
        keys = cut.split(" + ")
        kt = get_text_from_key(key)
        if map_from_qt_key(keys[-1]) != kt: continue
        broken = False
        for k in keys:
            if not map_from_qt_key(k) in pressed or not pressed[map_from_qt_key(k)]:
                broken = True
                break
        if broken: continue
        try:
            subprocess.call(s["Command"], shell=True)
            # subprocess.call(s["Command"].split(" "))
        except Exception as e:
            log(f"Error executing shortcut: {e}")
            

def on_release(key):
    log(f"Released: {get_text_from_key(key)}")
    pressed[get_text_from_key(key)] = False

keyboard_listener = None

def kb_listen():
    log("Verified listener thread")
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    log("Commencing listening...")
    keyboard_listener.start()

listener_thread = Thread(target=kb_listen)
listener_thread.daemon = True
listener_thread.start()
log("Started listener_thread")

def stop_icon(icon, item):
    if keyboard_listener: keyboard_listener.stop()
    icon.stop()

icon_data = Image.new('RGB', (64, 64), 'white')
try:
    with open(os.path.join(CDIR,"PyCutsTrayIcon.png" if sys.platform != "darwin" else "PyCutsTrayIconMono.png"), "rb") as f:
        icon_data = Image.open(f).copy()
except: pass
tray_menu = pystray.Menu(
    pystray.MenuItem("Open UI",run),
    pystray.MenuItem("Exit" if sys.platform != "darwin" else "Quit PyCuts",stop_icon)
)
icon = pystray.Icon('PyCuts', icon_data, 'PyCuts', tray_menu)

icon.run()
log("Exitting...")
listener_thread.join()
watch_thread.join()