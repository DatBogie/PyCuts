import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QInputDialog, QListWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = QWidget()
        self.setCentralWidget(central)
        
        main_lay = QVBoxLayout()
        central.setLayout(main_lay)
        
        self.ls = QListWidget()
        main_lay.addWidget(QLabel("Global Shortcuts"))
        
        btn_lay = QHBoxLayout()
        main_lay.addLayout(btn_lay)
        
        new = QPushButton("New")
        edit = QPushButton("Edit")
        delete = QPushButton("Delete")
        
        new.clicked.connect(self.new)
        
        btn_lay.addWidget(new)
        btn_lay.addWidget(edit)
        btn_lay.addWidget(delete)
        
        main_lay.addWidget(self.ls)
    def new(self):
        t, s = QInputDialog.getText(self,"PyCuts - New Shortcut","Enter shortcut's name:")
        if not s: return
        c, s = QInputDialog.getText(self,"PyCuts - New Shortcut","Enter command:")
        new = QListWidgetItem(t)
        new.setData(0,c)
        self.ls.addItem(new)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())