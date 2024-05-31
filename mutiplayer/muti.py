from PyQt6.QtWidgets import  QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QMessageBox,QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal,pyqtSlot,QTimer, QTime
from mutiplayer.client import clientGui,ConnectIP_port,Profile
from mutiplayer.server import ServerWindow
from mutiplayer.typeMassegeSocket import TypeMassnge
from mutiplayer.chat import Chat
from setting import operation as Op
from typing import List
# from game import Game
class Mutiplayer:
    
    def __init__(self,game) -> None:
        self.game =game
        self.ServerGUI = self.ServerGUIPage() 
        self.chat = self.ChatPage()
        self.__nowMatch = 0
    def start(self):
        self.__frame = self.newFrame()
        self.__frame.setTime(3)
        self.__frame.setMode("MultiPlayer Match 1")
        self.__frame.setMainTitle("START")
        self.__labelother = QLabel("  ".join(self.nowSetting["operation"]))
        self.__labelother.setObjectName("total")
        self.__labelother.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__frame.addOtherWidget(self.__labelother)
        self.newScore()
        self.GUIgame = GUIgameWindow()
        self.GUIgame.setPage(self.__frame)
        self.GUIgame.show()
        self.__countStartDown()
    def newScore(self):
        c=QHBoxLayout()
        for i in range(len(x:=self.Profiles)):
            pro = Profile(x[i].Player.name,x[i].Player.uuid,x[i].Player.ready,x[i].Player.score)
            pro.setVisible(True)
            pro.changeBg()
            pro.height()
            pro.inGame()
            c.addWidget(pro)
            if(i%10==0):
                self.__frame.addLayoutother(c)
                c = QHBoxLayout()
        self.__frame.addLayoutother(c)
    def setNowsetting(self,data:dict):
        self.nowSetting = data
    def setNumber(self,o:list):
        self.__numbers=o
    def setOp(self,O:list):
        self.__operations = O
    def setResult(self,o:list):
        self.__result =o
    def __countStartDown(self,timestart:int=3):
        self.timer = QTimer(self.__frame)
        self.time_left = QTime(0, 0, 0).addSecs(timestart)
        self.timer.timeout.connect(self.__updateDisplay)
        self.timer.start(1000)
    def __updateDisplay(self):
        self.time_left = self.time_left.addSecs(-1)
        self.__frame.setTime(self.time_left.toString("s"))

        if self.time_left == QTime(0, 0, 0):
            self.timer.stop()
            self.__frame.setTime(0)
            self.GameViewOneMatch()
            self.__timeofGameViewMatch()
    def GameViewOneMatch(self):
        self.__gui = self.game.GamePage()
        self.__gui.setDescriptionTop("Match 1 Step 1")
        self.__gui.setTotalOperation(self.nowSetting["operation"])
        self.__gui.setNumber(123)
        self.__gui.setOperation(Op("+"))
        self.GUIgame.setPage(self.__gui)
    def __timeofGameViewMatch(self):
        self.timer = QTimer(self.__gui)
        if type(self.nowSetting["timeofstep"]) == int:
            self.time_left = QTime(0, 0, 0).addSecs((self.nowSetting["step"]-1)*self.nowSetting["timeofstep"])
        else:
            self.time_left = QTime(0, 0, 0).addMSecs(int((self.nowSetting["step"]-1)*1000*self.nowSetting["timeofstep"]))
        self.timer.timeout.connect(self.__updateDisplayGameView)
        self.step=1
        self.__gui.setNumber(self.__numbers[self.__nowMatch][self.step-1])
        self.timer.start(int(1000*self.nowSetting["timeofstep"]))
        print(self.__numbers)
    def setProfilesList(self,list:List[Profile]):
        self.Profiles = list
    def __updateDisplayGameView(self):
        if type(self.nowSetting["timeofstep"]) == int:
            self.time_left = self.time_left.addSecs(self.nowSetting["timeofstep"])
        else:
            self.time_left = self.time_left.addMSecs(int(1000*self.nowSetting["timeofstep"]))
        try:
            if self.step%2==1:
                self.GUIgame.changebg1()
            else:
                self.GUIgame.changebg()
            self.__gui.setDescriptionTop(f"Match {self.__nowMatch+1} Step {self.step+1}")
            self.__gui.setNumber(self.__numbers[self.__nowMatch][self.step])
            self.__gui.setOperation(Op(self.__operations[self.__nowMatch][self.step-1]))
            print(self.__numbers[self.__nowMatch][self.step])
        except Exception as ER:
            self.timer.stop()
            self.GUIgame.changebg()
            self.send = self.game.AnswerPage()
            self.send.keyPressEvent = self.bank
            self.GUIgame.setPage(self.send)
            self.__timeofAnswer()
        self.step+=1 
    def __timeofAnswer(self):
        self.timer = QTimer(self.send)
        if type(self.nowSetting["timeofstep"]) == int:
            self.time_left = QTime(0, 0, 0).addSecs(self.nowSetting["timeanswer"]+2)
        else:
            self.time_left = QTime(0, 0, 0).addMSecs(int((self.nowSetting["timeanswer"]*1000)+2000))
        self.timer.timeout.connect(self.__updateDisplayAnswer)
        self.send.currentShow()
        self.send.setcurrent(str(self.nowSetting["timeanswer"]))
        self.can = True
        self.timer.start(int(1000))
    def __updateDisplayAnswer(self):
        if type(self.nowSetting["timeanswer"]) == int:
            self.time_left = self.time_left.addSecs(-1)
        else:
            self.time_left = self.time_left.addMSecs(-1000)
        self.send.setcurrent(str(int(self.time_left.toString("s"))-2))
        if self.time_left <= QTime(0, 0, 2):
            self.send.line.setDisabled(True)
            self.send.Showscoreadd()
            self.checkresultisCorrect()
            self.can = False
        if self.time_left == QTime(0, 0, 0):
            if self.__nowMatch+1 == self.nowSetting["match"]:
                self.GUIgame.close()
                self.__nowMatch=0
            else:
                self.__nowMatch+=1
                self.__frame =self.newFrame()
                self.GUIgame.setPage(self.__frame)
                self.__frame.setTime(3)
                self.__frame.setMode(f"MultiPlayer Match {self.__nowMatch+1}")
                self.__frame.setMainTitle("NEWMATCH")
                self.newScore()
                self.__countStartDown()
    def checkresultisCorrect(self):
        self.TypeM = TypeMassnge()
        try:
            x = int(self.send.line.text())
            if x ==(self.__result[self.__nowMatch]):
                self.send.setcurrent("Correct "+str(self.__result[self.__nowMatch]))
                self.send.score.setText("+ "+str(self.nowSetting["swin"]))
                
                if self.can:
                    data = {"type":TypeMassnge.Type.GAMECONTROLL.value,
                            "action":TypeMassnge.ActionGameControll.UPDATESCORE.value,
                            "name":self.name,
                            "uuid":self.TypeM.UUID(),
                            "up":self.nowSetting["swin"]}
                    
                    self.sendServer(self.TypeM.encodeByte(data=data))
            elif x<=(self.__result[self.__nowMatch]+self.nowSetting["rangenumb"]) and x>=(self.__result[self.__nowMatch]-self.nowSetting["rangenumb"]):
                self.send.setcurrent("You closer "+str(self.__result[self.__nowMatch]))
                self.send.score.setText("+ "+str(self.nowSetting["scloser"]))
                if self.can:
                    data = {"type":TypeMassnge.Type.GAMECONTROLL.value,
                            "action":TypeMassnge.ActionGameControll.UPDATESCORE.value,
                            "name":self.name,
                            "uuid":self.TypeM.UUID(),
                            "up":self.nowSetting["scloser"]}
                    self.sendServer(self.TypeM.encodeByte(data=data))
            else:
                self.send.setcurrent("Incorrect "+str(self.__result[self.__nowMatch]))
                self.send.score.setText("+ 0")
        except ValueError:
            self.send.setcurrent("Incorrect "+str(self.__result[self.__nowMatch]))
            self.send.score.setText("+ 0")
    def setName(self,name):
        self.name = name
    def bank(self,even):
        pass
    def getGUIgameWindow(self)->QMainWindow:
        return self.GUIgame
    def getFrame(self):
        return self.__frame
    def newFrame(self)->QWidget:
        return self.game.FramePage()
    def MutimenuPage(self):
        return Mutimenu(self)
    def closeChat(self):
        self.chat.close()
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
    def newSetting(self):
        return self.game.newSetting()
    def SettingGUIPage(self,setting,multi:bool=False):
        return self.game.SettingGUIPage(setting,multi)
    def Kick(self):
        self.a = QMessageBox()
        self.a.setText("You were kicked out of the room by the master.")
        self.a.show()
    def setSendServer(self,o):
        self.send1 = o
    def sendServer(self,data:bytes):
        self.send1(data)
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

class GUIgameWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(self.css())
        self.setObjectName("my")
        self.FullScreen(True)
    def FullScreen(self,b:bool):
        if b:
            self.setWindowState(Qt.WindowState.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowState.WindowActive)
    def setPage(self,n:QWidget):
        self.setCentralWidget(n)
    def css(self)->str:
        a=""
        with open("font.css") as f:
            a = f.read()
            f.close()
        return a
    def changebg1(self):
        self.setStyleSheet(self.css()+"""QMainWindow#my {
            background-color: rgb(14, 5, 25);
        }
        """)
    def changebg(self):
        self.setStyleSheet(self.css())
    