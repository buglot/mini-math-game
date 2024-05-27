from PyQt6.QtWidgets import  QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal,pyqtSlot
from mutiplayer.client import clientGui,ConnectIP_port
from mutiplayer.server import ServerWindow
from mutiplayer.chat import Chat
# from game import Game
class Mutiplayer:
    def __init__(self,game) -> None:
        self.game =game
        self.ServerGUI = self.ServerGUIPage() 
        self.chat = self.ChatPage()
    def start(self):
        pass
    def MutimenuPage(self):
        return Mutimenu(self)
    def ClientRoomPage(self,master=True,Server:ServerWindow=None):
        
        self.ServerGUI = self.ServerGUIPage()
        self.clinetRoom = clientGui(master=master,Server=Server,chat=self.chat)
        self.clinetRoom.setgame(self)
        return self.clinetRoom
    def ConnectPage(self):
        return ConnectIP_port(self)
    def ServerGUIPage(self):
        return ServerWindow()
    def ChatPage(self):
        return Chat()
    def setPage(self,page:QWidget):
        self.game.setPage(page)
class Mutimenu(QWidget):
    def __init__(self,Muti:Mutiplayer) -> None:
        super().__init__()
        lay = QVBoxLayout()
        self.Muti = Muti
        self.game = Muti.game
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
        self.Muti.setPage(self.game.MenuMainPage())
    def __connectserverAction(self):
        self.Muti.setPage(self.Muti.ConnectPage())

    def __createserverAction(self):
        self.Muti.setPage(self.Muti.ClientRoomPage(Server=self.Muti.ServerGUI))

