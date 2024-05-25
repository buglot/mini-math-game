from PyQt6.QtWidgets import  QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal,pyqtSlot
from mutiplayer.client import clientGui,ConnectIP_port
from mutiplayer.server import ServerWindow
# from game import Game
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
        self.__back = QPushButton("Back Play")
        lay.addWidget(self.__connectserver)
        lay.addWidget(self.__createSever)
        lay.addWidget(self.__back)
        self.setLayout(lay)
        self.__createSever.clicked.connect(self.__createserverAction)
        self.__connectserver.clicked.connect(self.__connectserverAction)
        self.__back.clicked.connect(self.__backmenuplay)
    def __backmenuplay(self):
        self.game.setPage(self.game.MenuMainPage())
    def __connectserverAction(self):
        self.__Connect = ConnectIP_port(self.game)
        self.game.setPage(self.__Connect)

    def __createserverAction(self):
        self.__client = clientGui(master=True)
        self.__client.setgame(self.game)
        self.game.setPage(self.__client)

