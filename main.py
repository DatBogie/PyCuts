import os, sys, json
from pynput import keyboard
from ui import mk_config_dir

mk_config_dir()

modifiers = {
    "cmd":False,
    "alt":False,
    "ctrl":False
}

def on_press(key):
    try:
        modifiers[key.name] = True
    except:pass

def on_release(key):
    try:
        modifiers[key.name] = False
    except:pass

# Set up the keyboard listener
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()