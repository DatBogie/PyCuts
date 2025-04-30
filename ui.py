import sys, os, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QTimer
from KeyboardDialog import KeyboardDialog, getTextFromQKeyEvent

def get_config_dir():
    return os.path.join(os.path.expanduser("~"),".config","pycuts") if sys.platform != "win32" else os.path.join(os.path.expanduser("~"),"AppData","Local","PyCuts")

LOAD_DATA = None
if os.path.exists(get_config_dir()) and os.path.exists(os.path.join(get_config_dir(),"config.json")):
    with open(os.path.join(get_config_dir(),"config.json"),"r") as f:
        LOAD_DATA = json.load(f)

def mk_config_dir():
    p = get_config_dir()
    if os.path.exists(p): return
    def_data = []
    os.makedirs(p)
    with open(os.path.join(p,"config.json"),"w") as f:
        json.dump(def_data,f,indent=4)

mk_config_dir()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400,200)
        self.setFixedSize(400,200)
        central = QWidget()
        self.setCentralWidget(central)
        
        main_lay = QVBoxLayout()
        central.setLayout(main_lay)
        
        self.ls = QTableWidget()
        main_lay.addWidget(QLabel("Global Shortcuts"))
        self.ls.setRowCount(0)
        self.ls.setColumnCount(3)
        self.ls.setHorizontalHeaderLabels(["Name","Command","Shortcut"])
        
        btn_lay = QHBoxLayout()
        main_lay.addLayout(btn_lay)
        
        new = QPushButton("New")
        edit = QPushButton("Edit Shortcut")
        delete = QPushButton("Delete")
        
        new.clicked.connect(self.new)
        edit.clicked.connect(self.edit_current_shortcut)
        delete.clicked.connect(self.del_row)
        
        btn_lay.addWidget(new)
        btn_lay.addWidget(edit)
        btn_lay.addWidget(delete)
        
        if LOAD_DATA:
            self.ls.setRowCount(len(LOAD_DATA))
            self.ls.setColumnCount(len(LOAD_DATA[0].keys()))
            for row, x in enumerate(LOAD_DATA):
                t, c, k = x["Name"], x["Command"], x["Shortcut"]
                self.ls.setItem(row,0,QTableWidgetItem(t))
                self.ls.setItem(row,1,QTableWidgetItem(c))
                self.ls.setItem(row,2,QTableWidgetItem(k))
                
        
        main_lay.addWidget(self.ls)
    def new(self):
        t, s = QInputDialog.getText(self,"PyCuts - New Shortcut","Enter shortcut's name:")
        if not s: return
        c, s = QInputDialog.getText(self,"PyCuts - New Shortcut",f"Shortcut '{t}'\nEnter command:")
        if not s: return
        k, s = KeyboardDialog.getShortcut(self, "PyCuts - New Shortcut",f"Shortcut '{t}'\nPress shortcut key(s):")
        if not s or not k: return   
        self.ls.setRowCount(self.ls.rowCount()+1)
        self.ls.setItem(self.ls.rowCount()-1,0,QTableWidgetItem(t))
        self.ls.setItem(self.ls.rowCount()-1,1,QTableWidgetItem(c))
        # self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(getTextFromQKeyEvent(k)))
        self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(" + ".join([getTextFromQKeyEvent(x) for x in k.values()])))
        QTimer.singleShot(1000,self.save_data)
    def edit_current_shortcut(self):
        row = self.ls.currentRow()
        k, s = KeyboardDialog.getShortcut(self, "PyCuts - Edit Shortcut",f"Shortcut '{self.ls.item(row,0).text()}'\nPress shortcut key(s):")
        if not s or not k: return
        self.ls.setItem(row,2,QTableWidgetItem(" + ".join([getTextFromQKeyEvent(x) for x in k.values()])))
        self.save_data()
    def del_row(self):
        btn = QMessageBox.warning(self,"PyCuts = Remove Shortcut",f"Are you sure you want to delete '{self.ls.item(self.ls.currentRow(),0).text()}'?",QMessageBox.StandardButton.Yes,QMessageBox.StandardButton.No)
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
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    exit_code = app.exec()
    win.save_data()
    sys.exit(exit_code)