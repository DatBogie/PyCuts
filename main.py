import os, sys, json
from pynput import keyboard
from ui import mk_config_dir, get_config_dir
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

pressed = {}

SHORTCUTS = []

def update_shortcuts():
    global SHORTCUTS
    with open(os.path.join(get_config_dir(),"config.json")) as f:
        SHORTCUTS = json.load(f)



def on_press(key):
    try:
        pressed[key.name] = True
    except:
        pressed[key.char] = True

def on_release(key):
    try:
        pressed[key.name] = False
    except:
        pressed[key.char] = False

# Set up the keyboard listener
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()
keyboard_listener.join()