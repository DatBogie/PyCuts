import sys
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

def getTextFromQKeyEvent(x:QKeyEvent):
    return "Tab" if x.key() == Qt.Key.Key_Backtab else Qt.Key(x.key()).name[4:]

class btnIgnoreKeys(QPushButton):
    def __init__(self, text:str="", parent:QWidget=None):
        super().__init__(text,parent)
    def keyPressEvent(self, a0):
        a0.ignore()

class KeyboardDialog(QDialog):
    def __init__(self, parent=None, mode:int=0):
        super().__init__(parent)
        self.setFixedSize(250,125)
        
        self.awaitingInput = False
        self.mode = mode
        self.data = {} if mode == 1 else None
        self.btn = btnIgnoreKeys()
        self.btn.clicked.connect(self.startListening)
        self.label = QLabel()

        main_lay = QVBoxLayout()
        main_lay.addWidget(self.label)
        main_lay.addWidget(self.btn)

        cancel = QPushButton("Cancel")
        ok = QPushButton("OK")
        
        cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        ok.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self.accept)

        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        
        if sys.platform == "darwin":
            btn_lay.addWidget(cancel)
            btn_lay.addWidget(ok)
        else:
            btn_lay.addWidget(ok)
            btn_lay.addWidget(cancel)

        main_lay.addLayout(btn_lay)

        self.setLayout(main_lay)
        self.installEventFilter(self)

    class DialogMode():
        SINGLE_KEY = 0
        SHORTCUT = 1

    def keyPressEvent(self, a0):
        if not self.awaitingInput: return super().keyPressEvent(a0)
        if self.mode == 0:
            self.data = a0.clone()
            self.stopListening()
        else:
            self.data[getTextFromQKeyEvent(a0)] = a0.clone()
            # if not getTextFromQKeyEvent(a0).upper() in Qt.Modifier._member_names_:
                # self.stopListening()
        self.btn.setText(f"({self.updateText()})")
    def keyReleaseEvent(self, a0):
        if not self.awaitingInput: return super().keyReleaseEvent(a0)
        if self.mode == 0: return
        return
        if getTextFromQKeyEvent(a0) in self.data:
            self.data.pop(getTextFromQKeyEvent(a0))
        self.btn.setText(f"({self.updateText()})")
    def eventFilter(self, a0, a1):
        if type(a1) == QKeyEvent:
            if a1.key() == Qt.Key.Key_Tab:
                if a1.type() == QKeyEvent.Type.KeyPress:
                    self.keyPressEvent(a1)
                else:
                    self.keyReleaseEvent(a1)
                return False
        return super().eventFilter(a0, a1)

    def updateText(self) -> str:
        if self.mode == 0:
            txt = getTextFromQKeyEvent(self.data)
        else:
            txt = " + ".join(self.data.keys())
        self.btn.setText(txt)
        return txt
    def startListening(self):
        if self.awaitingInput:
            return self.stopListening()
        if self.mode == 1: self.data.clear()
        self.btn.setText("(...)")
        self.awaitingInput = True
    def stopListening(self):
        self.awaitingInput = False
        self.updateText()

    @staticmethod
    def getKey(parent:QWidget=None,title:str="",label:str="") -> tuple[QKeyEvent|None, bool]:
        dia = KeyboardDialog(parent,KeyboardDialog.DialogMode.SINGLE_KEY)
        dia.setWindowTitle(title)
        dia.label.setText(label)
        result = dia.exec()
        return dia.data, result == QDialog.DialogCode.Accepted
    @staticmethod
    def getShortcut(parent:QWidget=None,title:str="",label:str="") -> tuple[dict[str,QKeyEvent], bool]:
        dia = KeyboardDialog(mode=KeyboardDialog.DialogMode.SHORTCUT)
        dia.setWindowTitle(title)
        dia.label.setText(label)
        result = dia.exec()
        return dia.data, result == QDialog.DialogCode.Accepted
