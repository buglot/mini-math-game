import socket
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget,QLabel,QPushButton,QHBoxLayout,QLineEdit,QGridLayout,QScrollArea,QCheckBox
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread,Qt
from mutiplayer.server import ServerWindow
from mutiplayer.chat import Chat
from typing import List
from mutiplayer.typeMassegeSocket import TypeMassnge,Player
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
            while self.running:
                try:
                    data = {"type":TypeMassnge.Type.SYSTEMCALL.value}
                    data["action"] = TypeMassnge.ActionSystemCall.PING.value
                    data["name"] = self.name
                    Type1 = TypeMassnge()
                    data["uuid"]=Type1.UUID()
                    self.s.send(Type1.encode(data).encode())
                    self.checkServerAlive.emit(True)
                except Exception as E:
                    print("checking Error:",E)
                    self.checkServerAlive.emit(False)
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
        
        self.__profiles = Profiles()

        # left
        self.__title = QLabel("Mutiplayer")
        self.__title.setObjectName("multi")
        self.report = QLabel("")
        self.report.setObjectName("reportmulti")
        self.__numb = QLabel("people in room : 0")
        self.__numb.setObjectName("reportmulti")
        self.ch = QPushButton("c")
        self.ch.setToolTip("open chat")
        self.ch.setObjectName("c")
        self.ch.setMaximumSize(50,50)
        self.ch.clicked.connect(self.chat.show)
        self.__listpeoplename = QLabel()
        # row
        self.__ready = QPushButton("Ready")
        self.__ready.setObjectName("mutiready")
        self.__ready.setDisabled(True)
        self.__ready.clicked.connect(self.__readybuttonAction)
        self.__butclose = QPushButton("Exit Room")
        self.__butclose.clicked.connect(self.closebuttonEvent)

        #right
        self.__settingTitle = QLabel("Setting Game")
        self.scrollarea = QScrollArea()
        row1 = QGridLayout()

        #layout
        col1_row1 =QVBoxLayout()
        self.col2_row1 = QVBoxLayout()
        layoutcolreport = QVBoxLayout()
        layout2 = QVBoxLayout()
        self.rowlistPlayroom = QHBoxLayout()
        self.scrollareaplayper = QScrollArea()

        #add widget or layoyut
        col1_row1.addWidget(self.__title)
        col1_row1.addLayout(layoutcolreport)
        self.col2_row1.addWidget(self.__settingTitle)
        self.col2_row1.addWidget(self.scrollarea)
        
        layoutcolreport.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutcolreport.addWidget(self.report)
        layoutcolreport.addWidget(self.__numb)
        layoutcolreport.addWidget(self.ch)
        
        row1.addLayout(col1_row1,0,0)
        row1.addLayout(self.col2_row1,0,1)
        layout2.addLayout(row1)
        layout2.addWidget(self.scrollareaplayper)
        layout2.addWidget(self.__ready)
        layout2.addWidget(self.__butclose)


        self.mytype = TypeMassnge()
        self.mytype.SystemCallActionEven.connect(self.SystemCallActionEven)
        self.mytype.ChatActionEven.connect(self.___chatAction)
        self.mytype.GameControllActionEven.connect(self.__gameAction)
        self.setLayout(layout2)
        self.chat.massnge_send.connect(self.__chat_massnge_send)
        self.chat.show()
        if(self.__master):
            self.serverview = Server
            self.serverview.show()
            self.serverview.startServer()
            self.serverview.ServerIsStarted.connect(self.__ConnectServer)
            self.serverview.ServerIsTabClose.connect(self.__dochecker)
        else:
            self.__ConnectServer(False)
    def __gameAction(self,data:dict):
        match TypeMassnge.ActionGameControll(data["action"]):
            case TypeMassnge.ActionGameControll.SETTING:
                self.nowSettingGame = data
                self.settingGUI.setALLSettingView(data)
            case TypeMassnge.ActionGameControll.READY:
                self.__profiles.setready(Player(data["name"],data["uuid"]),data["ready"])
    def ___chatAction(self,data:dict):
        if self.mytype.UUID() == data["uuid"] and self.name == data["name"]:
            self.__linechat =self.chat.chatlineMe(data["msg"])
        else:
            self.__linechat =self.chat.chatline(data["msg"],data["name"])
        self.chat.addChat(self.__linechat)    
    @pyqtSlot(str)
    def __chat_massnge_send(self,msg:str):
        data = {"type":TypeMassnge.Type.CHAT.value,"name":self.name,"uuid":self.mytype.UUID(),"msg":msg}
        if self.canChat:
            self.socket_thread.send(self.mytype.encode(data=data).encode())
        else:
            self.chat.addChat(self.chat.chatline("Cant send to server disconnect server","chatSystem"))

    @pyqtSlot(dict)
    def SystemCallActionEven(self,data:dict):
        match TypeMassnge.ActionSystemCall(data["action"]):
            case TypeMassnge.ActionSystemCall.GETLISTPEOPLE:
                self.__profiles.clear()
                rowlistPlayroom = QHBoxLayout()
                widget =QWidget()
                widget.setLayout(rowlistPlayroom)
                for x in data["data"]:
                    profile = Profile(x[0],x[1],x[3],x[2])
                    self.__profiles.addList(profile)
                    rowlistPlayroom.addWidget(self.__profiles.getWidget()[-1])
                self.__numb.setText("people in room : "+str(data["nPeople"]))
                self.scrollareaplayper.setWidget(widget)
    def setServerGUI(self,gui:ServerWindow):
        self.serverview = gui
    def setgame(self,muti):
        self.muti = muti
        self.setting = self.muti.newSetting()
        self.settingGUI = self.muti.SettingGUIPage(self.setting,True)
        self.settingGUI.OnlyView()
        self.scrollarea.setWidget(self.settingGUI)
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
    def sendReadyProfile(self,b:bool):
        data = {"type":TypeMassnge.Type.GAMECONTROLL.value,
                "action":TypeMassnge.ActionGameControll.READY.value,
                "name":self.name,
                "uuid":self.mytype.UUID(),
                "ready":b
                }
        return data
    def callPlayer(self):
        data = {"type":TypeMassnge.Type.SYSTEMCALL.value,
                "action":TypeMassnge.ActionSystemCall.CALL_LISTPEOPLE.value}
        return data
    def callGameSetting(self):
        data = {"type":TypeMassnge.Type.GAMECONTROLL.value,
                "action":TypeMassnge.ActionGameControll.GETSETTING.value}
        return data
    @pyqtSlot(int)
    def update_connection_status(self, connected):
        if connected==1:
            self.report.setText("Connected to the server.")
            self.canChat = True
            self.socket_thread.send(self.mytype.encode(self.joinServer()).encode())
            if self.__master:
                self.socket_thread.send(self.mytype.encodeByte(self.sendReadyProfile(True)))
            self.socket_thread.send(self.mytype.encode(self.callPlayer()).encode())
            self.socket_thread.send(self.mytype.encode(self.callGameSetting()).encode())
            self.__ready.setDisabled(False)
        elif connected==2:
            self.report.setText("Connecting......")
            self.__ready.setDisabled(True)
        else:
            self.report.setText("disconnected to the server.")
            self.__ready.setDisabled(True)
            self.canChat =False
    def closebuttonEvent(self):
        self.socket_thread.stop()
        if self.__master:
            self.serverview.close()
        self.muti.closeChat()
        self.muti.setPage(self.muti.MutimenuPage())
    def closeEvent(self, event):
        if self.__master:
            self.serverview.close()
        self.muti.closeChat()
        super().closeEvent(event)
    def __dochecker(self, b: bool):
        if not b:
            self.report.setText("disconnected to the server.")
            self.__ready.setDisabled(True)
            self.canChat =False
            self.socket_thread.stop()
            self.checker.stop()

    def __readybuttonAction(self):
        self.socket_thread.send(self.mytype.encodeByte(self.sendReadyProfile(True)))
class Profile(QWidget):
    def __init__(self, name, uuid, read,score) -> None:
        super().__init__()
        self.setObjectName("multiWidget")
        self.Player = Player(name,uuid)
        self.Player.ready = read
        self.Player.score = score
        self.name =QLabel(name)
        self.name.setObjectName("nameMultiplayer")
        self.score =QLabel(str(self.Player.score))
        self.ready = QCheckBox()
        self.ready.setChecked(self.Player.ready)
        self.checking(self.Player.ready)
        self.ready.stateChanged.connect(self.__ready_stateChanged)
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.score)
        layout.addWidget(self.ready)
        self.setLayout(layout)
   
    def update(self):
        self.score.setText(str(self.Player.score))
        self.ready.setChecked(self.Player.ready)
    def __ready_stateChanged(self,r):
        self.checking(Qt.CheckState(r)==Qt.CheckState.Checked)

    def checking(self,b:bool):
        if b:
            self.ready.setText("Ready")
        else:
            self.ready.setText("Not ready")
class Profiles:
    __playerlist : List[Profile]
    def __init__(self) -> None:
        self.__playerlist = []
    def addList(self,p:Profile):
        self.__playerlist.append(p)
    def isAllready(self) -> bool:
        return all(player.Player.ready for player in self.__playerlist)
    def setready(self,p:Player,b:bool):
          for x in self.__playerlist:
            if x.Player.uuid == p.uuid and x.Player.name == p.name:
                x.Player.ready = b
                x.update()
                break
    def clear(self):
        self.__playerlist = []
    def drop(self,p:Player):
        for x in self.__playerlist:
            if x.Player.uuid == p.uuid and x.Player.name == p.name:
                self.__playerlist.remove(p)
                x.close()
                break
    def scoreUp(self,n:int,p:Player):
         for x in self.__playerlist:
            if x.Player.uuid == p.uuid and x.Player.name == p.name:
                x.Player.upscore(n)
                x.update()
                break
    
    def getWidget(self) ->List[Profile]:
        return  self.__playerlist
