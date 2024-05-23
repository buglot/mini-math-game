from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtWidgets import QWidget,QPushButton,QLabel,QLineEdit,QHBoxLayout,QVBoxLayout,QMainWindow,QMessageBox
from setting import Setting,guisetting,operation as Op
from typing import List
import math
import random
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
        


        # layout add widget
        self.__layoutrow1.addLayout(self.__layoutcolinrow1)
        self.__layoutcolinrow1.addWidget(self.__description)
        self.__layoutcolinrow1.addWidget(self.__totalOperation)
        self.__boxtop = QWidget()
        self.__boxtop.setLayout(self.__layoutrow1)
        self.__boxtop.setMaximumHeight(80)
        self.__layoutcol.addWidget(self.__boxtop)
        
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

    def start(self,mode=1):
        if mode ==2:
            pass
        else:
            self.__generateGamge()
            self.onGameScreen(False)

            self.gui = GameGUI(1)
            self.gui.setDescriptionTop("Match 1 Step 1")
            self.gui.setTotalOperation(self.setting.getSetting()["operation"])
            self.gui.setNumber(123)
            self.gui.setOperation(Op("+"))
            self.setPage(self.gui)

           
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
                else:
                    listnum.append(w)
                    result+=str(w)
                
                    

            self.__numbers.append(listnum)
            self.__operations.append(listope)
            self.__result.append(round(eval(result)))
        print(self.__numbers,self.__operations,self.__result)
                

    
        

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
        self.menu = font(Game(showsetting=self.showSetting,setPage=self.setPage,setting=set,onGameScreen=self.ongamescreen))
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
    def css(self)->str:
        a=""
        with open("font.css") as f:
            a = f.read()
            f.close()
        return a