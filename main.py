import os, sys, multiprocessing
from ui import mk_config_dir, get_config_dir, get_local_dir, MainWindow
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QCoreApplication
from handler import handler

mk_config_dir()

def log(*args):
    print(" ".join([str(x) for x in list(args)]),"\n")
    with open(os.path.join(get_config_dir(),"latest.log"),"a") as f:
        f.write("\n")
        for x in list(args):
            f.write(" "+str(x))

CDIR = os.path.abspath("./") if not hasattr(sys,"_MEIPASS") else sys._MEIPASS
log(f"CDIR={CDIR}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if os.path.exists(os.path.join(CDIR,"__LOCK__")):
        os.remove(os.path.join(CDIR,"__LOCK__"))
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # tray = QSystemTrayIcon(QIcon(os.path.join(CDIR,"icons","PyCutsTrayIcon.png" if sys.platform != "darwin" else "PyCutsTrayIconMono.png")),parent=app)
    tray_icon = QIcon(os.path.join(CDIR,"icons","PyCutsTrayIconMono.png") if sys.platform == "darwin" else os.path.join(get_local_dir(),"icon.png"))
    tray = QSystemTrayIcon(tray_icon,parent=app)
    tray.setToolTip("PyCuts")

    def close():
        with open(os.path.join(CDIR,"__BREAK__"),"w") as f:
            f.write("")
        tray.hide()
        QCoreApplication.quit()

    tray_menu = QMenu()

    win = None

    def run():
        global win
        if not win: win = MainWindow()
        win.show()
        win.raise_()
        win.activateWindow()

    open_ui = QAction("Open UI")
    open_ui.triggered.connect(run)
    tray_menu.addAction(open_ui)

    exit_act = QAction("Exit" if sys.platform != "darwin" else "Quit PyCuts")
    exit_act.triggered.connect(close)
    tray_menu.addAction(exit_act)

    tray.setContextMenu(tray_menu)
    tray.show()
    
    process = multiprocessing.Process(target=handler)
    process.start()

    app.exec()
    log("Exitting main...")
    process.join()
    
    if os.path.exists(os.path.join(CDIR,"__LOCK__")):
        os.remove(os.path.join(CDIR,"__LOCK__"))
    if os.path.exists(os.path.join(CDIR,"__BREAK__")):
        os.remove(os.path.join(CDIR,"__BREAK__"))