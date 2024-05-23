from PyQt6.QtCore import Qt,pyqtSignal,QTimer, QTime
from PyQt6.QtWidgets import QWidget,QPushButton,QLabel,QLineEdit,QHBoxLayout,QVBoxLayout,QMainWindow,QMessageBox,QStyle
from setting import Setting,guisetting,operation as Op
from typing import List
import random
class Answer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(self.css())
        self.__mode = QLabel("Answer")
        self.__mode.setObjectName("mode")
        self.__mode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__line =QLineEdit()
        self.__layoutcol = QVBoxLayout()
        self.__layoutcol.addWidget(self.__mode)
        self.__layoutcol.addWidget(self.__line)
        self.__currect = QLabel()
        self.__currect.setObjectName("time")
        self.__layoutcol.addWidget(self.__currect)
        self.__currect.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__currect.setVisible(False)
        self.__line.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.__line.setFocus()
        self.__buttonnext = QPushButton("next")
        self.__buttonnext.setVisible(False)
        self.__layoutcol.addWidget(self.__buttonnext)
        self.setLayout(self.__layoutcol)
    def addActionDoWhenEnterkey(self,func):
        self.dosomeEnter =func
    def addActionDoWhenRkey(self,func):
        self.dosome =func
        self.__buttonnext.clicked.connect(self.dosome)
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.dosomeEnter()
        if event.key() in (Qt.Key.Key_R,Qt.Key.Key_End):
            self.dosome()
    def setcurrent(self,n):
        self.__currect.setText(n)
    def currentShow(self):
        self.__currect.setVisible(True)
        self.__buttonnext.setVisible(True)
    def getAnswer(self)->str:
        return self.__line.text()
    def css(self)->str:
        a=""
        with open("GameGUI.css") as f:
            a = f.read()
            f.close()
        return a
class Frame(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(self.css())
        # label
        self.__mode = QLabel()
        self.__start = QLabel()
        self.__time = QLabel()

        # objectnameofcss
        self.__mode.setObjectName("mode")
        self.__start.setObjectName("maintitle")
        self.__time.setObjectName("time")

        #Align label
        self.__mode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__start.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
       
        #layout
        self.__layoutcol = QVBoxLayout()
        self.__layoutother = QHBoxLayout()

        self.__layoutcol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layoutcol.addWidget(self.__mode)
        self.__layoutcol.addWidget(self.__start)
        self.__layoutcol.addWidget(self.__time)
        self.__layoutcol.addLayout(self.__layoutother)
        self.setLayout(self.__layoutcol)
    def addOtherWidget(self,w:QWidget):
        self.__layoutother.addWidget(w)
    def setMode(self,msg:str):
        self.__mode.setText(msg)
    def setTime(self,n:str|int):
        self.__time.setText(str(n))
    def setMainTitle(self,msg:str):
        self.__start.setText(msg)
    def css(self)->str:
        a=""
        with open("GameGUI.css") as f:
            a = f.read()
            f.close()
        return a
class GameGUI(QWidget):
    __number : QLabel
    __description :QLabel
    __totalOperation : QLabel
    def __init__(self,step:int) -> None:
        super().__init__()
        self.step = step
        self.setStyleSheet(self.css())
        #LabelObject
        self.__number = QLabel()
        self.__description = QLabel()
        self.__totalOperation = QLabel()
        # Alignment label
        self.__number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__description.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__totalOperation.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #objectname for css
        self.__description.setObjectName("des") # QLabel#des {color:red} in css
        self.__totalOperation.setObjectName("total")
        self.__number.setObjectName("num") 
        #layout
        self.__layoutcol = QVBoxLayout()
        self.__layoutrow1 = QHBoxLayout()
        self.__layoutcolinrow1 = QVBoxLayout()
        self.__layoutrow2 = QHBoxLayout()
        

        #Aliglayout
        self.__layoutrow1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__layoutrow2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout add widget
        self.__layoutrow1.addLayout(self.__layoutcolinrow1)
        self.__layoutcolinrow1.addWidget(self.__description)
        self.__layoutcolinrow1.addWidget(self.__totalOperation)
        
        self.__box = QWidget()
        self.__box.setLayout(self.__layoutrow1)
        self.__box.setMaximumHeight(90)
        self.__layoutcol.addWidget(self.__box)
        self.__layoutrow2.addWidget(self.__number)
        self.__layoutcol.addLayout(self.__layoutrow2)

        self.setLayout(self.__layoutcol)

    def setNumber(self,n:int|str):
        self.__number.setText(str(n))
    def setOperation(self,n : Op):
        self.__number.setText(str(n.value)+self.__number.text())
    def setDescriptionTop(self,msg:str):
        self.__description.setText(msg)
    def setTotalOperation(self,list:list):
        result = "  ".join(list)
        if len(list)==1:
            self.__totalOperation.setText("only "+result)
        else:
            self.__totalOperation.setText(result) 
    def css(self)->str:
        a=""
        with open("GameGUI.css") as f:
            a = f.read()
            f.close()
        return a
class Game:
    __numbers : List[List[int]]
    __operations : List[List[Op]]
    __result : List[int|float]
    def __init__(self,setting:Setting,setPage,showsetting,onGameScreen) -> None:
        self.setting = setting
        self.setPage = setPage
        self.showsetting = showsetting
        self.onGameScreen = onGameScreen
        self.__nowMatch = 0
    def start(self,mode=1):
        if mode ==2:
            pass
        else:
            self.__generateGamge()
            self.onGameScreen(False)
            self.__frame = Frame()
            self.__frame.setTime(3)
            self.__frame.setMode("Solo Match 1")
            self.__frame.setMainTitle("START")
            self.__labelother = QLabel("  ".join(self.setting.getSetting()["operation"]))
            self.__labelother.setObjectName("total")
            self.__labelother.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.__frame.addOtherWidget(self.__labelother)
            self.setPage( self.__frame)
            self.__nowMatch = 0
            self.__countStartDown()

            
    def GameViewOneMatch(self):
        self.__gui = GameGUI(1)
        self.__gui.setDescriptionTop("Match 1 Step 1")
        self.__gui.setTotalOperation(self.setting.getSetting()["operation"])
        self.__gui.setNumber(123)
        self.__gui.setOperation(Op("+"))
        self.setPage(self.__gui)
    
    def __timeofGameViewMatch(self):
        self.timer = QTimer(self.__gui)
        if type(self.setting.getSetting()["timeofstep"]) == int:
            self.time_left = QTime(0, 0, 0).addSecs((self.setting.getSetting()["step"]-1)*self.setting.getSetting()["timeofstep"])
        else:
            self.time_left = QTime(0, 0, 0).addMSecs(int((self.setting.getSetting()["step"]-1)*1000*self.setting.getSetting()["timeofstep"]))
        self.timer.timeout.connect(self.__updateDisplayGameView)
        self.step=1
        self.__gui.setNumber(self.__numbers[self.__nowMatch][self.step-1])
        self.timer.start(int(1000*self.setting.getSetting()["timeofstep"]))
        
        print(self.__numbers)
    def __updateDisplayGameView(self):
        
        if type(self.setting.getSetting()["timeofstep"]) == int:
            self.time_left = self.time_left.addSecs(self.setting.getSetting()["timeofstep"])
        else:
            self.time_left = self.time_left.addMSecs(int(1000*self.setting.getSetting()["timeofstep"]))
        try:
            if self.step%2==1:
                self.changebg1()
            else:
                self.changebg()
            self.__gui.setDescriptionTop(f"Match {self.__nowMatch+1} Step {self.step+1}")
            self.__gui.setNumber(self.__numbers[self.__nowMatch][self.step])
            self.__gui.setOperation(self.__operations[self.__nowMatch][self.step-1])
            print(self.__numbers[self.__nowMatch][self.step])
        except:
            self.timer.stop()
            self.onGameScreen(False)
            self.send = Answer()
            self.setPage(self.send)
            self.send.addActionDoWhenEnterkey(self.showCurrent)
            self.send.addActionDoWhenRkey(self.ActionwhensendR)
        self.step+=1 
    def showCurrent(self):
        self.send.currentShow()
        self.send.setcurrent(str(self.__result[self.__nowMatch]))
    def ActionwhensendR(self):
        if self.__nowMatch+1 == self.setting.getSetting()["match"]:
            self.setPage(font(self))
        else:
            self.__nowMatch+=1
            self.__frame =Frame()
            self.setPage(self.__frame)
            self.__frame.setTime(3)
            self.__frame.setMode(f"Solo Match {self.__nowMatch+1}")
            self.__frame.setMainTitle("NEWMATCH")
            self.__countStartDown()
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
            self.onGameScreen(True)
            self.GameViewOneMatch()
            self.__timeofGameViewMatch()
    def __generateGamge(self):
        setting = self.setting.getSetting()
        self.__numbers = []
        self.__operations =[]
        self.__result = []
        matchgame = setting["match"]
        digit = setting["digit"]
        step = setting["step"]
        operation = setting["operation"]
        for matchgame_ in range(matchgame):
            listnum = []
            listope = []
            result =""
            for x in range(step):
                if x>0:
                    op = Op(random.choice(operation))
                    listope.append(op)
                    if op == Op.Division:
                        result+="/"
                    elif op == Op.Multiplication:
                        result+="*"
                    else:
                        result+=op.value
                if (w:=round(random.random()*(10**digit))) == 0:
                    listnum.append(1)
                    result+="1"
                    result = str(round(eval(result)))
                else:
                    listnum.append(w)
                    result+=str(w)
                    result = str(round(eval(result)))
                # print(result)
            self.__numbers.append(listnum)
            self.__operations.append(listope)
            self.__result.append(round(eval(result)))
        # print(self.__numbers,self.__operations,self.__result)
    def addDefualtDB(self,n):
        self.defualtbg =n
    def addBG(self,n):
        self.setBg =n     
    def changebg1(self):
        self.setBg(self.defualtbg+"""QMainWindow#my {
            background-color: rgb(20, 9, 25);
        }
        """)
    def changebg(self):
        self.setBg(self.defualtbg)
    def CheckCanRunning(self)->bool:
        self.setting.loadSave()
        if self.setting.operation1ormore():
            return True
        return False
class font(QWidget):
    def __init__(self,Game:Game) -> None:
        super().__init__()

        self.game = Game
        self.layout1 =  QVBoxLayout()
        self.labeltitlegame = QLabel("i dont know what is name of game")
        self.labeltitlegame.setMaximumHeight(50)
        self.buttonplay1 = QPushButton("Play")
        self.buttonsetting = QPushButton("Setting")
        self.layout1.addWidget(self.labeltitlegame)
        self.layout1.addWidget(self.buttonplay1)
        self.layout1.addWidget(self.buttonsetting)
        self.setLayout(self.layout1)
        self.buttonsetting.clicked.connect(self.game.showsetting)
        self.buttonplay1.clicked.connect(self.buttonplay)
    def buttonplay(self):
        self.game.setPage(menuplay(self.game))

class menuplay(QWidget):
    def __init__(self,Game:Game) -> None:
        super().__init__()
        self.setObjectName("bg")
        self.game=Game
        self.layout1 =  QVBoxLayout()
        self.setLayout(self.layout1)
        self.buttonsolo = QPushButton("solo")
        self.buttonmutiplayer = QPushButton("mutiplayer")
        self.buttonback = QPushButton("Back Mainmenu")
        self.layout1.addWidget(self.buttonsolo)
        self.layout1.addWidget(self.buttonmutiplayer)
        self.layout1.addWidget( self.buttonback)
        self.buttonback.clicked.connect(self.__buttonblackaction)
        self.buttonsolo.clicked.connect(self.__buttonsoloClickAction)
    def __buttonblackaction(self):
        self.game.setPage(font(self.game))
    def __buttonsoloClickAction(self):
        if self.game.CheckCanRunning():
            self.game.start()
        else:
            self.a=QMessageBox()
            self.a.setText("not operation can you back to setting")
            self.a.show()

class GameWindow(QMainWindow):
    def __init__(self,set:Setting) -> None:
        super().__init__()
        self.setObjectName("my")
        self.setStyleSheet(self.css())
        self.page =1
        self.setWindowTitle("Game")
        self.guisetting = guisetting(set)
        self.setMinimumSize(500,500)
        self.__game =Game(showsetting=self.showSetting,setPage=self.setPage,setting=set,onGameScreen=self.ongamescreen)
        self.__game.addBG(self.setBgcolor)
        self.__game.addDefualtDB(self.styleSheet())
        self.menu = font(self.__game)
        
        self.setCentralWidget(self.menu)
    def showSetting(self):
        self.guisetting.show()
    def setPage(self,n:QWidget):
        self.setCentralWidget(n)
    def ongamescreen(self,b:bool):
        if b:
            self.setWindowState(Qt.WindowState.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowState.WindowActive)
    def setBgcolor(self,css:str):
        self.setStyleSheet(css)
    def css(self)->str:
        a=""
        with open("font.css") as f:
            a = f.read()
            f.close()
        return a