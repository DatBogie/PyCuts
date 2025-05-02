import sys, os, json, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QTableWidget, QTableWidgetItem, QMessageBox, QListWidget, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from KeyboardDialog import KeyboardDialog, getTextFromQKeyEvent
from pynput import keyboard

CDIR = os.path.abspath("./") if not hasattr(sys,"_MEIPASS") else sys._MEIPASS

def get_text_from_key(key):
    try:
        return key.name
    except:
        return key.char

def get_config_dir():
    return os.path.join(os.path.expanduser("~"),".config","pycuts") if sys.platform != "win32" else os.path.join(os.path.expanduser("~"),"AppData","Local","PyCuts")

LOAD_DATA = None
if os.path.exists(get_config_dir()) and os.path.exists(os.path.join(get_config_dir(),"config.json")):
    with open(os.path.join(get_config_dir(),"config.json"),"r") as f:
        LOAD_DATA = json.load(f)

def mk_config_dir():
    p = get_config_dir()
    if os.path.exists(p):
        with open(os.path.join(p,"latest.log"),"w") as f:
            f.write("")
        return
    def_data = []
    os.makedirs(p)
    with open(os.path.join(p,"config.json"),"w") as f:
        json.dump(def_data,f,indent=4)
    with open(os.path.join(p,"latest.log"),"w") as f:
        f.write("")

mk_config_dir()

class squareBtn(QPushButton):
    def resizeEvent(self, a0):
        size = min(a0.size().width(),a0.size().height())
        self.setFixedSize(size,size)
        super().resizeEvent(a0)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCuts")
        self.setMinimumSize(400,200)
        central = QWidget()
        self.setCentralWidget(central)
        
        try:
            self.setWindowIcon(QIcon(os.path.join(CDIR,"PyCutsTrayIcon.png")))
        except: pass
        
        main_lay = QVBoxLayout()
        central.setLayout(main_lay)
        
        self.ls = QTableWidget()
        lbl = QLabel("Global Shortcuts")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(lbl)
        
        self.ls.setRowCount(0)
        self.ls.setColumnCount(3)
        self.ls.setHorizontalHeaderLabels(["Name","Command","Shortcut"])
        
        btn_lay = QHBoxLayout()
        main_lay.addLayout(btn_lay)
        
        new = QPushButton("New")
        new.setToolTip("Register new global shortcut")
        edit = QPushButton("Edit Shortcut")
        edit.setToolTip("Edit selected global shortcut")
        delete = QPushButton("Delete")
        delete.setToolTip("Delete selected global shortcut")
        helpbtn = squareBtn("?")
        helpbtn.setToolTip("See list of all valid keys")
        
        new.clicked.connect(self.new)
        edit.clicked.connect(self.edit_current_shortcut)
        delete.clicked.connect(self.del_row)
        helpbtn.clicked.connect(self.show_help)
        
        btn_lay.addWidget(new)
        btn_lay.addWidget(edit)
        btn_lay.addWidget(delete)
        btn_lay.addWidget(helpbtn)
        
        self.ls.setColumnCount(3)
        
        self.help_menu = QWidget()
        self.help_menu.setWindowTitle("Keys - PyCuts")
        
        help_main_lay = QVBoxLayout()
        self.help_menu.setLayout(help_main_lay)
        
        self.help_filter = QLineEdit()
        help_main_lay.addWidget(self.help_filter)
        self.help_filter.textEdited.connect(self.help_filter_text)
        
        self.help_list = QListWidget()
        items = [*[getTextFromQKeyEvent(x) for x in Qt.Key],*[get_text_from_key(x) for x in keyboard.Key]]
        items.sort()
        self.help_list.addItems(items)
        help_main_lay.addWidget(self.help_list)
        
        if LOAD_DATA:
            try:
                self.ls.setRowCount(len(LOAD_DATA))
                for row, x in enumerate(LOAD_DATA):
                    t, c, k = x["Name"], x["Command"], x["Shortcut"]
                    self.ls.setItem(row,0,QTableWidgetItem(t))
                    self.ls.setItem(row,1,QTableWidgetItem(c))
                    self.ls.setItem(row,2,QTableWidgetItem(k))
            except Exception as e:
                print(f"Failed to load config file: {e}")
                self.ls.setRowCount(0)
                print(f"Backing up current config file to {os.path.join(get_config_dir(),f"config{int(time.time())}.json.bak")}")
                
        
        main_lay.addWidget(self.ls)
    def new(self):
        t, s = QInputDialog.getText(self,"New Shortcut - PyCuts","Enter shortcut's name:")
        if not s: return
        c, s = QInputDialog.getText(self,"New Shortcut - PyCuts",f"Shortcut '{t}'\nEnter command:")
        if not s: return
        k, s = KeyboardDialog.getShortcut(self, "New Shortcut - PyCuts",f"Shortcut '{t}'\nPress shortcut key(s):")
        if not s or not k: return
        self.ls.setRowCount(self.ls.rowCount()+1)
        self.ls.setItem(self.ls.rowCount()-1,0,QTableWidgetItem(t))
        self.ls.setItem(self.ls.rowCount()-1,1,QTableWidgetItem(c))
        # self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(getTextFromQKeyEvent(k)))
        self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(" + ".join([x for x in k.values()])))
        self.save_data()
    def edit_current_shortcut(self):
        row = self.ls.currentRow()
        if row == -1: return
        k, s = KeyboardDialog.getShortcut(self, "Edit Shortcut - PyCuts",f"Shortcut '{self.ls.item(row,0).text()}'\nPress shortcut key(s):")
        if not s or not k: return
        self.ls.setItem(row,2,QTableWidgetItem(" + ".join([x for x in k.values()])))
        self.save_data()
    def del_row(self):
        if self.ls.currentRow() == -1: return
        btn = QMessageBox.warning(self,"Remove Shortcut - PyCuts",f"Are you sure you want to delete '{self.ls.item(self.ls.currentRow(),0).text()}'?",QMessageBox.StandardButton.Yes,QMessageBox.StandardButton.No)
        if btn == QMessageBox.StandardButton.Yes:
            self.ls.removeRow(self.ls.currentRow())
        self.save_data()
        
    def save_data(self):
        data = []
        for row in range(self.ls.rowCount()):
            data.append({})
            for col in range(self.ls.columnCount()):
                item = self.ls.item(row,col)
                data[row][self.ls.horizontalHeaderItem(col).text()] = item.text()
        print(f"Saving data : {data}...")
        try:
            with open(os.path.join(get_config_dir(),"config.json"), "w") as f:
                json.dump(data,f,indent=4)
        except Exception as e:
            print(f"Failed to save: {e}")
    
    def show_help(self):
        self.help_menu.show()
        
    def help_filter_text(self):
        txt = self.help_filter.text()
        for i in range(self.help_list.count()):
            item = self.help_list.item(i)
            item.setHidden(not (txt == "" or item.text().lower().find(txt.lower()) != -1))
        
def run():
    win = MainWindow()
    win.show()
    win.save_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    exit_code = app.exec()
    win.save_data()
    sys.exit(exit_code)