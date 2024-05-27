import socket
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget,QLabel,QPushButton,QHBoxLayout,QLineEdit
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread,Qt
from mutiplayer.server import ServerWindow
from mutiplayer.chat import Chat
from mutiplayer.typeMassegeSocket import TypeMassnge
# from game import Game
class SocketServerisAlive(QThread):
    checkServerAlive = pyqtSignal(bool)
    def __init__(self, s,name:str):
        super().__init__()
        self.s = s
        self.running = True
        self.name= name
    def run(self):
            print("checker runing")
            count = 0
            while self.running:
                try:
                    data = {"type":TypeMassnge.Type.SYSTEMCALL.value}
                    data["action"] = TypeMassnge.ActionSystemCall.PING.value
                    data["name"] = self.name
                    Type1 = TypeMassnge()
                    data["uuid"]=Type1.UUID()
                    self.s.send(Type1.encode(data).encode())
                    self.checkServerAlive.emit(True)
                    count = 0
                except Exception as E:
                    print("checking Error:",E)
                    self.checkServerAlive.emit(False)
                    count+=1
                    if count ==10:
                        break
                QThread.sleep(5)
                    
    def stop(self):
        self.running=False
class SocketThread(QThread):
    message_received = pyqtSignal(str)
    connection_status_changed = pyqtSignal(int)
    noData = pyqtSignal(bool)
    client_connected = pyqtSignal(socket.socket)
    def __init__(self, host="localhost",port=3430):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True
        self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        try:
            self.connection_status_changed.emit(2)
            self.s.connect((self.host, self.port))
            self.connection_status_changed.emit(1)
            self.client_connected.emit(self.s)
            while self.running:
                data = self.s.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    self.message_received.emit(message)
                else:
                    self.noData.emit(True)
                    break
        except ConnectionError as e:
            print(f"Connection error: {e}")
            self.connection_status_changed.emit(0)
        except Exception as e:
            print(f"Connection error: {e}")
            self.connection_status_changed.emit(0)
    def send(self,s):
        self.s.send(s)
    def stop(self):
        self.running = False
        self.s.close()
        self.connection_status_changed.emit(0)
    def getS(self):
        return self.s

class ConnectIP_port(QWidget):
    def __init__(self,muti):
        super().__init__()
        layout2 = QVBoxLayout()
        self.muti = muti
        self.game = muti.game
        self.ip = QLineEdit()
        self.ip.setPlaceholderText("IP")
        self.port =QLineEdit()
        self.port.setPlaceholderText("Port")
        self.name = QLineEdit()
        self.name.setPlaceholderText("Your Name")
        self.button = QPushButton("connect")
        self.back = QPushButton("Back Mutiplay")
        self.port.editingFinished.connect(self.__portmustbeInt)
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(self.ip)
        layout2.addWidget(self.port)
        layout2.addWidget(self.name)
        layout2.addWidget(self.button)
        layout2.addWidget(self.back)
        self.setLayout(layout2)
        self.button.clicked.connect(self.__connect)
        self.back.clicked.connect(self.__back)
    def __back(self):
        self.muti.setPage(self.muti.MutimenuPage())
    def __connect(self):
        if self.ip.text() !="" or self.port.text() != "":
            game = clientGui(self.ip.text(),port=int(self.port.text()),name=self.name.text(),chat=self.muti.ChatPage())
            game.setgame(self.muti)
            self.game.setPage(game)
    def __portmustbeInt(self):
        try:
            int(self.port.text())
        except ValueError as E:
            self.port.clear()
            self.port.setPlaceholderText("plz enter port is only number")
class clientGui(QWidget):
    def __init__(self,host="localhost",port=3430,name="Master",master=False,Server:ServerWindow=None,chat:Chat=None):
        super().__init__()
        self.__master = master
        self.port=port
        self.host=host
        self.name = name
        self.chat = chat
        self.setWindowTitle('Connect Server')
        self.__title = QLabel("Mutiplayer")
        self.report = QLabel("")
        self.__numb = QLabel("people in room : 0")
        self.__numberReady = QLabel("")
        self.__listpeoplename = QLabel()
        self.__ready = QPushButton("Ready")
        self.__ready.setObjectName("mutiready")
        self.__ready.setDisabled(True)
        self.__butclose = QPushButton("Exit Room")
        self.__butclose.clicked.connect(self.closebuttonEvent)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.__title)
        layout2.addWidget(self.report)
        layout2.addWidget(self.__numb)
        layout2.addWidget(self.__listpeoplename)
        layout2.addWidget(self.__numberReady)
        layout2.addWidget(self.__ready)
        layout2.addWidget(self.__butclose)
        self.mytype = TypeMassnge()
        self.mytype.SystemCallActionEven.connect(self.SystemCallActionEven)
        self.mytype.ChatActionEven.connect(self.___chatAction)
        self.setLayout(layout2)
        self.chat.massnge_send.connect(self.__chat_massnge_send)
        self.chat.show()
        if(self.__master):
            self.serverview = Server
            self.serverview.show()
            self.serverview.startServer()
            self.serverview.ServerIsStarted.connect(self.__ConnectServer)
        else:
            self.__ConnectServer(False)
    def ___chatAction(self,data:dict):
        if self.mytype.UUID() == data["uuid"] and self.name == data["name"]:
            self.__linechat =self.chat.chatlineMe(data["msg"])
        else:
            self.__linechat =self.chat.chatline(data["msg"],data["name"])
        self.chat.addChat(self.__linechat)    
    @pyqtSlot(str)
    def __chat_massnge_send(self,msg:str):
        data = {"type":TypeMassnge.Type.CHAT.value,"name":self.name,"uuid":self.mytype.UUID(),"msg":msg}
        self.socket_thread.send(self.mytype.encode(data=data).encode())


    @pyqtSlot(dict)
    def SystemCallActionEven(self,data:dict):
        match TypeMassnge.ActionSystemCall(data["action"]):
            case TypeMassnge.ActionSystemCall.GETLISTPEOPLE:
                print("client 152",data)
                self.__numb.setText("people in room : "+str(data["nPeople"]))
    def setServerGUI(self,gui:ServerWindow):
        self.serverview = gui
    def setgame(self,muti):
        self.muti = muti
    def __ConnectServer(self,b):
        if b:
            self.port = self.serverview.getPort()
            self.host = self.serverview.getHost()
        self.socket_thread = SocketThread(self.host,self.port)
        self.socket_thread.message_received.connect(self.display_message)
        self.socket_thread.connection_status_changed.connect(self.update_connection_status)
        self.socket_thread.client_connected.connect(self.notdata)
        self.socket_thread.start()
        self.checker = SocketServerisAlive(self.socket_thread.getS(),self.name)
        self.checker.checkServerAlive.connect(self.__dochecker)
    
    @pyqtSlot(str)
    def display_message(self, message):
        self.mytype.isType(message)
    @pyqtSlot(socket.socket)
    def notdata(self,b):
        self.checker.start()
    def joinServer(self)->dict:
        data = {"type":TypeMassnge.Type.SYSTEMCALL.value,
                "action":TypeMassnge.ActionSystemCall.JOIN.value,
                "name":self.name,
                "uuid":self.mytype.UUID()}
        return data
    def callPlayer(self):
        data = {"type":TypeMassnge.Type.SYSTEMCALL.value,
                "action":TypeMassnge.ActionSystemCall.CALL_LISTPEOPLE.value}
        return data
    @pyqtSlot(int)
    def update_connection_status(self, connected):
        if connected==1:
            self.report.setText("Connected to the server.")
            
            self.socket_thread.send(self.mytype.encode(self.joinServer()).encode())
            self.socket_thread.send(self.mytype.encode(self.callPlayer()).encode())
            self.__ready.setDisabled(False)
        elif connected==2:
            self.report.setText("Connecting......")
        else:
            self.report.setText("disconnected to the server.")
            self.__ready.setDisabled(True)
    def closebuttonEvent(self):
        self.socket_thread.stop()
        if self.__master:
            self.serverview.close()
        self.muti.setPage(self.muti.MutimenuPage())
    def closeEvent(self, event):
        if self.__master:
            self.serverview.close()
        self.chat.close()
        super().closeEvent(event)
    def __dochecker(self, b: bool):
        if not b:
            self.report.setText("disconnected to the server.")
            self.__ready.setDisabled(True)
        
        print(b)
            