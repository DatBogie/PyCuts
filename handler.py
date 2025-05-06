def handler():
    import os, sys, json, subprocess
    from pynput import keyboard
    from ui import mk_config_dir, get_config_dir, get_text_from_key
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    mk_config_dir()

    def log(*args):
        print(" ".join([str(x) for x in list(args)]),"\n")
        with open(os.path.join(get_config_dir(),"latest.log"),"a") as f:
            f.write("\n")
            for x in list(args):
                f.write(" "+str(x))

    CDIR = os.path.abspath("./") if not hasattr(sys,"_MEIPASS") else sys._MEIPASS
    log(f"CDIR={CDIR}")
    
    if os.path.exists(os.path.join(CDIR,"__LOCK__")):
        log("__LOCK__ present; quitting...")
        raise Exception
    else:
        with open(os.path.join(CDIR,"__LOCK__"),"w") as f:
                f.write("")

    class FileChangedHandler(FileSystemEventHandler):
        def __init__(self, path:str):
            super().__init__()
            self.path = path
        
        def on_modified(self, event):
            if event.src_path.endswith(self.path):
                update_shortcuts()

    pressed = {}

    MAP = { # Qt => pynput
        "Meta": ["cmd",None],
        "Control": [["ctrl","blacklist",["win32"]],["ctrl_l","whitelist",["win32"]]],
        "Alt": ["alt_l","whitelist",["win32"]],
        "CapsLock": ["caps_lock",None]
    }

    def map_from_qt_key(key:str): # `key` is `str` from `Qt.Key`
        if key in MAP.keys():
            if type(MAP[key][0]) == str:
                if MAP[key][1] == "blacklist":
                    if sys.platform in MAP[key][2]: return key
                elif MAP[key][1] == "whitelist":
                    if not sys.platform in MAP[key][2]: return key
                return MAP[key]
            else:
                for set in MAP[key]:
                    if set[1] == "blacklist":
                        if sys.platform in set[1]: continue
                    elif set[1] == "whitelist":
                        if not sys.platform in set[2]: continue
                    return set[0]
                return key
        return key.lower()

    SHORTCUTS = []

    def update_shortcuts():
        nonlocal SHORTCUTS
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
                log("Executing:",s["Command"])
                subprocess.Popen(s["Command"], shell=True)
            except Exception as e:
                log(f"Error executing shortcut: {e}")

    def on_release(key):
        log(f"Released: {get_text_from_key(key)}")
        pressed[get_text_from_key(key)] = False

    log("Verified listener thread")
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    log("Commencing listening...")
    keyboard_listener.start()

    handler = FileChangedHandler("config.json")
    observer = Observer()
    observer.schedule(handler,get_config_dir(),recursive=False)
    observer.start()
    log("Watchdog started...")

    if os.path.exists(os.path.join(CDIR,"__BREAK__")):
        os.remove(os.path.join(CDIR,"__BREAK__"))

    while not os.path.exists(os.path.join(CDIR,"__BREAK__")):
        pass

    log("Exitting...")
    
    os.remove(os.path.join(CDIR,"__BREAK__"))

    observer.stop()
    keyboard_listener.stop()