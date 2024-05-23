import json
import os
from PyQt6.QtCore import QEvent,Qt
from    PyQt6.QtWidgets import QWidget,QPushButton,QLabel,QLineEdit,QHBoxLayout,QVBoxLayout,QCheckBox,QMessageBox
from enum import Enum
class Rand:
    def __init__(self,start,end) -> None:
        self.start = start 
        self.end = end
    def getNum(self)->list:
        return range(self.start,self.end+1)
    def __str__(self) -> str:
        return "Rand_"+self.start+"_"+self.end
class operation(Enum):
    Addition = "+"
    Subtraction = "-"
    Multiplication = "x"
    Division = "÷"
    Modulus = "%"
    # def __repr__(self):
    #     return self.value
class Setting:
    __mydict: dict
    def __init__(self) -> None:
        self.__path = os.path.join("setting.json")
        self.loadSave()
    def loadSave(self):
        self.__jsonload = json.JSONDecoder()
        if (self.ExistSave()==False):
            self.SaveDefualtSetting()
        s = ""
        with open(self.__path) as f :
           s= f.read()
           f.close()
        self.__mydict = self.__jsonload.decode(s)
        if type(self.__mydict["digit"])==type(str):
            pass 
    def getSetting(self)->dict:
        return self.__mydict 
    def operation1ormore(self)->bool:
        if len(self.__mydict["operation"]) >0:
            return True
        return False
    def setMatch(self,n:int)->None:
        if type(n) != int:
            raise Exception("Put number match you want to play")
            
        self.__mydict["match"] = n
    
    def setdigit(self,n:int|Rand):
        if type(n) != int and type(n) !=Rand:
            raise Exception("Put number for digit to play or custom range digit")
        self.__mydict["digit"] = n

    def setStep(self,n:int|float)->None:
        if type(n) != int:
             raise Exception("Put number for step number you can see")
        self.__mydict["step"] = n

    def addOperation(self,n:operation):
        self.__mydict["operation"].append(n.value)
    def dropOperation(self,n:operation):
        self.__mydict["operation"].pop(self.__mydict["operation"].index(n.value))
    def setTimeofStep(self,n:int|float):
        if type(n) != int and type(n) !=float:
            raise Exception("Put number for time seconds you can see")
        self.__mydict["timeofstep"] = n
    def ExistSave(self)->bool:
        return os.path.exists(self.__path)
    def SaveDefualtSetting(self)->None:
        self.__endocode = json.JSONEncoder()
        self.__defulat = self.__endocode.encode(self.getDefualtsetting())
        with open(self.__path,"w+") as f:
            f.write(self.__defulat)
            f.close()
        self.__mydict = self.getDefualtsetting()
    def getDefualtsetting(self)->dict:
        return {"match":1,
                "digit":1,
                "step":5,
                "timeofstep":1,
                "operation":["+"]
                }
    def SaveSetting(self)->None:
        self.__endocode = json.JSONEncoder()
        self.__defulat = self.__endocode.encode(self.__mydict)
        with open(self.__path,"w+") as f:
            f.write(self.__defulat)
            f.close()
class guisetting(QWidget):
    def __init__(self,setting:Setting) -> None:
        super().__init__()
        self.setObjectName("my")
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)
        self.setWindowTitle("Setting Game")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        # setting
        self.__setting = setting
        self.__setting.loadSave() # new loading for sure
        
        self.__dataSetting = self.__setting.getSetting()
        self.setStyleSheet(self.css())
        # layout
        self.__layoutcol = QVBoxLayout()
        self.__layoutrow1 = QHBoxLayout()
        self.__layoutrow = QHBoxLayout()
        self.__layoutrow2 = QHBoxLayout()
        self.__layoutrow3 = QHBoxLayout()
        self.__layoutrow4 = QHBoxLayout()
        self.__layoutrow5 = QVBoxLayout()
        self.__layoutrow5_1 = QHBoxLayout()
        # button
        self.__savebutton = QPushButton("Save")
        self.__savebutton.setObjectName("save")
        self.__savebutton.clicked.connect(self.__savebuttonActionClick)
     
        self.__loaddefault = QPushButton("LOAD Default")
        self.__loaddefault.setObjectName("load")
        self.__loaddefault.clicked.connect(self.__loaddefaultbuttonActionClick)

        # lineEdit
        self.__lineEdit = QLineEdit(str(self.__dataSetting["match"]))
        self.__lineEdit.editingFinished.connect(self.__lineeditChangeAction)

        self.__lineEditdigit = QLineEdit(str(self.__dataSetting["digit"]))
        self.__lineEditdigit.editingFinished.connect(self.__lineeditdigitChangeAction)

        self.__lineEditstep = QLineEdit(str(self.__dataSetting["step"]))
        self.__lineEditstep.editingFinished.connect(self.__lineeditstepChangeAction)

        self.__lineEdittimeofstep = QLineEdit(str(self.__dataSetting["timeofstep"]))
        self.__lineEdittimeofstep.editingFinished.connect(self.__lineedittimeofstepChangeAction)

        #ckeckbox

        self.checkboxes = []
        for opera in operation:
            
            checkbox = QCheckBox(opera.value)
            try:
                self.__dataSetting["operation"].index(opera.value)
                checkbox.setChecked(True)
            except Exception:
                pass
            
            checkbox.stateChanged.connect(self.check)
            self.__layoutrow5_1.addWidget(checkbox)
            self.checkboxes.append(checkbox)
    
        # addinlayoutrow
        self.__layoutrow.addWidget(self.__savebutton)
        self.__layoutrow.addWidget(self.__loaddefault)

        self.__layoutrow1.addWidget(QLabel("Match:"))
        self.__layoutrow1.addWidget(self.__lineEdit)

        self.__layoutrow2.addWidget(QLabel("Digit:"))
        self.__layoutrow2.addWidget(self.__lineEditdigit)

        self.__layoutrow3.addWidget(QLabel("Step:"))
        self.__layoutrow3.addWidget(self.__lineEditstep)

        self.__layoutrow4.addWidget(QLabel("TimeofStep"))
        self.__layoutrow4.addWidget(self.__lineEdittimeofstep)
        self.label =QLabel("Operation")
        self.label.setMaximumHeight(30)
        self.__layoutrow5.addWidget(self.label)
        self.__layoutrow5.addLayout(self.__layoutrow5_1)


        # layoutcol add layoutrow
        self.__layoutcol.addLayout(self.__layoutrow1)
        self.__layoutcol.addLayout(self.__layoutrow2)
        self.__layoutcol.addLayout(self.__layoutrow3)
        self.__layoutcol.addLayout(self.__layoutrow4)
        self.__layoutcol.addLayout(self.__layoutrow5)
        self.__layoutcol.addLayout(self.__layoutrow)

        # add layout in widget
        self.setLayout(self.__layoutcol)
    def __savebuttonActionClick(self,e):
        self.__setting.SaveSetting()
        self._a = QMessageBox()
        self._a.setText("Save done")
        self._a.show()
    def __loaddefaultbuttonActionClick(self):
        self.__dataSetting = self.__setting.getDefualtsetting()
        self.__lineEditdigit.setText(str(self.__dataSetting["digit"]))
        self.__lineEdit.setText(str(self.__dataSetting["match"]))
        self.__lineEditstep.setText(str(self.__dataSetting["step"]))
        self.__lineEdittimeofstep.setText(str(self.__dataSetting["timeofstep"]))
        for checkbox in self.checkboxes:
            try:
                self.__dataSetting["operation"].index(checkbox.text())
                checkbox.setChecked(True)
            except Exception:
                checkbox.setChecked(False)
    def __lineeditChangeAction(self):
        try:
            self.__setting.setMatch(int(self.__lineEdit.text()))
        except:
            self.__lineEdit.setText(str(1))
            self.__setting.setMatch(1)
    
    def __lineeditdigitChangeAction(self):
        try:
            self.__setting.setdigit(int(self.__lineEditdigit.text()))
        except:
            self.__lineEditdigit.setText(str(1))
            self.__setting.setdigit(1)
    
    def __lineeditstepChangeAction(self):
        try:
            self.__setting.setStep(int(self.__lineEditstep.text()))
        except:
            self.__lineEditstep.setText(str(5))
            self.__setting.setStep(5)

    def __lineedittimeofstepChangeAction(self):
        try:
            self.__setting.setTimeofStep(int(self.__lineEdittimeofstep.text()))
        except:
            try:
                self.__setting.setTimeofStep(float(self.__lineEdittimeofstep.text()))
            except:
                self.__lineEdittimeofstep.setText(str(1))
                self.__setting.setTimeofStep(1)

    def check(self,state:QEvent):
        sender = self.sender()
        if state == Qt.CheckState.Checked.value:
            print(f"{sender.text()} Checked")
            self.__setting.addOperation(operation(sender.text()))
        else:
            print(f"{sender.text()} Unchecked")
            self.__setting.dropOperation(operation(sender.text()))

    def css(self)->str:
        cssdata = ""
        with open("setting.css","r") as f:
            cssdata = f.read()
            f.close()
        return cssdata