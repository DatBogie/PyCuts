import os, sys, json
from pynput import keyboard
from ui import mk_config_dir, get_config_dir, get_text_from_key
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

mk_config_dir()

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

pressed = {}

MAP = {
    "meta": "cmd"
}

SHORTCUTS = []

def update_shortcuts():
    global SHORTCUTS
    with open(os.path.join(get_config_dir(),"config.json")) as f:
        SHORTCUTS = json.load(f)

def on_press(key):
    pressed[get_text_from_key(key)] = True
    print(get_text_from_key(key))

def on_release(key):
    pressed[get_text_from_key(key)] = False

# Set up the keyboard listener
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()
keyboard_listener.join()