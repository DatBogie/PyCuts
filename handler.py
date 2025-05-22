def handler():
    import os, sys, json, subprocess
    from pynput import keyboard
    from ui import mk_config_dir, get_config_dir, get_text_from_key
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    mk_config_dir()
    
    CONFIG_DIR = get_config_dir()

    def log(*args):
        with open(os.path.join(CONFIG_DIR,"latest.log"),"a") as f:
            message = "\n"
            for x in list(args):
                message+=" "+str(x)
            print(message)
            f.write(message)

    CDIR = os.path.abspath("./") if not hasattr(sys,"_MEIPASS") else sys._MEIPASS
    log(f"CDIR={CDIR}")
    
    LOCK_PATH = os.path.join(CDIR,"__LOCK__")
    
    if os.path.exists(LOCK_PATH):
        log("__LOCK__ present; quitting...")
        raise Exception
    else:
        with open(LOCK_PATH,"w"):pass
        
    class FileChangedHandler(FileSystemEventHandler):
        def __init__(self, path:str):
            super().__init__()
            self.path = path
        
        def on_modified(self, event):
            if event.src_path.endswith(self.path):
                update_shortcuts()
    
    observer1 = None
    class FileCreatedHandler(FileSystemEventHandler):
        def on_created(self, event):
            log("watchdog: file created")
            if event.src_path.endswith("__BREAK__"):
                log("watchdog: break...")
                observer1.stop()

    pressed = {}

    MAP = { # Qt => pynput
        "Meta": ["cmd",None],
        "Control": [["ctrl","blacklist",["win32"]],["ctrl_l","whitelist",["win32"]]],
        "Alt": ["alt_l","whitelist",["win32"]],
        "CapsLock": ["caps_lock",None]
    }

    def map_from_qt_key(key:str): # `key` is `str` from `Qt.Key`
        mapping = MAP.get(key)
        if not mapping: return key.lower()
        maps = mapping[0]
        if type(maps) == str:
            map_type = mapping[1]
            if map_type == "blacklist":
                if sys.platform in mapping[2]: return
            elif map_type == "whitelist":
                if not sys.platform in mapping[2]: return
            return maps
        else:
            for set in mapping:
                set_type = set[1]
                if set_type == "blacklist":
                    if sys.platform in set[2]: continue
                elif set_type == "whitelist":
                    if not sys.platform in set[2]: continue
                return set[0]
            return key


    SHORTCUTS = []

    def update_shortcuts():
        nonlocal SHORTCUTS
        with open(os.path.join(CONFIG_DIR,"config.json")) as f:
            SHORTCUTS = json.load(f)
            log("SHORTCUTS => ",SHORTCUTS)

    update_shortcuts()

    def on_press(key):
        # log(f"Pressed: {get_text_from_key(key)}")
        key_name = get_text_from_key(key)
        if pressed.get(key_name): return
        pressed[key_name] = True
        for s in SHORTCUTS:
            cut:str = s["Shortcut"]
            keys = cut.split(" + ")
            kt = key_name
            if map_from_qt_key(keys[-1]) != kt: continue
            broken = False
            for k in keys:
                mapped_key = map_from_qt_key(k)
                if not mapped_key in pressed.keys() or not pressed[mapped_key]:
                    broken = True
                    break
            if broken: continue
            try:
                log("Executing:",s["Command"])
                subprocess.Popen(s["Command"], shell=True)
            except Exception as e:
                log(f"Error executing shortcut: {e}")

    def on_release(key):
        # log(f"Released: {get_text_from_key(key)}")
        pressed[get_text_from_key(key)] = False

    log("Verified listener thread")
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    log("Commencing listening...")
    keyboard_listener.start()

    observer = Observer()
    observer1 = Observer()
    observer.schedule(FileChangedHandler("config.json"),CONFIG_DIR,recursive=False)
    observer1.schedule(FileCreatedHandler(),CDIR,recursive=False)
    observer.start()
    observer1.start()
    log("Watchdogs started...")
    
    BREAK_PATH = os.path.join(CDIR,"__BREAK__")

    if os.path.exists(BREAK_PATH):
        os.remove(BREAK_PATH)
    
    try:
        observer1.join()
    finally:
        log("Exitting handler...")
        
        os.remove(BREAK_PATH)

        keyboard_listener.stop()