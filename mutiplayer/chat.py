from PyQt6.QtWidgets import QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QWidget,QScrollArea,QApplication,QCheckBox
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot,QEvent
from PyQt6.QtGui import QKeyEvent
import sys

class Chat(QWidget):
    massnge_send = pyqtSignal(str)
    name:str
    uuid:str
    def __init__(self) -> None:
        super().__init__()
        Layout = QVBoxLayout()
        Layout.addWidget(QLabel("Chat Room"))
        self.setWindowTitle("Chat Room")
        self.Checkbox =QCheckBox()
        self.Checkbox.setText("Pin top")
        self.Checkbox.setChecked(True)
        self.Checkbox.checkStateChanged.connect(self.checkboxAction)
        self.setMinimumSize(300,300)
        self.ScrollArea = QScrollArea()
        self.ScrollArea.setLayout(QVBoxLayout())
        self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ScrollArea.setWidgetResizable(True)
        self.box = QWidget()
        self.box.setLayout(QVBoxLayout())
        self.layoutbox = self.box.layout()
        self.layoutbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ScrollArea.setWidget(self.box)
        Layout.addWidget(self.ScrollArea)
        self.sendbox = QLineEdit()
        self.sendbox.setPlaceholderText('"send" Enter')
        Layout.addWidget(self.sendbox)
        self.ScrollArea.verticalScrollBar().rangeChanged.connect(lambda: self.ScrollArea.verticalScrollBar().setValue(self.ScrollArea.verticalScrollBar().maximum()))
        self.setLayout(Layout)
        self.setStyleSheet(self.css())
    def checkboxAction(self,e):
        if e== Qt.CheckState.Checked:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,True)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()
    def keyPressEvent(self,q:QKeyEvent):
        if q.key() ==Qt.Key.Key_Enter or q.key() ==Qt.Key.Key_Return:
            if self.__notIsEmty():
                self.massnge_send.emit(self.sendbox.text())
                self.sendbox.setText("")
    def chatlineMe(self,msg:str)->QWidget:
        self.__chatline = QWidget()
        self.__chatline.setObjectName("chatme")
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        la = QLabel(msg)
        la.setObjectName("chat")
        layout.addWidget(la)
        self.__chatline.setLayout(layout)
        return self.__chatline
    def chatline(self,msg:str,name:str="dont")->QWidget:
        self.__chatline = QWidget()
        self.__chatline.setObjectName("chatOther")
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        name1 = QLabel(name+" : ")
        name1.setObjectName("name")
        layout.addWidget(name1)
        la = QLabel(msg)
        la.setObjectName("chat")
        layout.addWidget(la)
        self.__chatline.setLayout(layout)
        return self.__chatline
    def __notIsEmty(self)->bool:
        if self.sendbox.text() !="":
            return True
        return False

    def addChat(self,q:QWidget):
        self.layoutbox.addWidget(q)
    def css(self)->str:
        a=""
        with open("chat.css") as f:
            a = f.read()
            f.close()
        return a
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    gui = Chat()
    gui.show()
    sys.exit(app.exec())