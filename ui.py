import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QTableWidget, QTableWidgetItem
from KeyboardDialog import KeyboardDialog, getTextFromQKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

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
        delete = QPushButton("Delete")
        
        new.clicked.connect(self.new)
        delete.clicked.connect(self.del_row)
        
        btn_lay.addWidget(new)
        btn_lay.addWidget(delete)
        
        main_lay.addWidget(self.ls)
    def new(self):
        t, s = QInputDialog.getText(self,"PyCuts - New Shortcut","Enter shortcut's name:")
        if not s: return
        c, s = QInputDialog.getText(self,"PyCuts - New Shortcut","Enter command:")
        if not s: return
        k, s = KeyboardDialog.getShortcut(self, "PyCuts - New Shortcut","Press shortcut key:")
        if not s or not k: return   
        self.ls.setRowCount(self.ls.rowCount()+1)
        self.ls.setItem(self.ls.rowCount()-1,0,QTableWidgetItem(t))
        self.ls.setItem(self.ls.rowCount()-1,1,QTableWidgetItem(c))
        # self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(getTextFromQKeyEvent(k)))
        self.ls.setItem(self.ls.rowCount()-1,2,QTableWidgetItem(" + ".join([getTextFromQKeyEvent(x) for x in k.values()])))
    def del_row(self):
        self.ls.removeRow(self.ls.currentRow())
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())