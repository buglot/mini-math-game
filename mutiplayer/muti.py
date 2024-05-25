from PyQt6.QtWidgets import  QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal,pyqtSlot
from mutiplayer.client import clientGui
from mutiplayer.server import ServerWindow
class Mutiplayer:
    def __init__(self) -> None:
        pass
    def start(self):
        pass


class Mutimenu(QWidget):
    def __init__(self,game) -> None:
        super().__init__()
        lay = QVBoxLayout()
        self.game = game
        self.__connectserver = QPushButton("Connect Server")
        self.__createSever = QPushButton("Create Server")
        lay.addWidget(self.__connectserver)
        lay.addWidget(self.__createSever)
        self.setLayout(lay)
        self.__createSever.clicked.connect(self.__createserverAction)
        self.__connectserver.clicked.connect(self.__connectserverAction)
        
    def __connectserverAction(self):
        self.__client = clientGui()
        self.__client.closeClient.connect(self.__clientClose)
        self.game.setPage(self.__client)

    @pyqtSlot(bool)
    def __clientClose(self,b:bool):
        print(b)
        self.game.setPage(self)
    def __createserverAction(self):
        self.__client = clientGui(master=True)
        self.__client.closeClient.connect(self.__clientClose)
        self.game.setPage(self.__client)
        