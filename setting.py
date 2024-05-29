import json
import os
from typing import List
from PyQt6.QtCore import QEvent,Qt,pyqtSignal
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
    __multi:dict
    def __init__(self) -> None:
        self.__path = os.path.join("setting.json")
        self.loadSave()
        self.__multi = self.getMultiDefualtsetting()
        self.updateMulti()
        
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
    def updateMulti(self):
        self.__multi.update(self.__mydict)
    def SettingISDefualtSetting(self):
        self.__mydict = self.getDefualtsetting()
    def getSettingMulti(self)->dict:
        return self.__multi
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
    def setMulti(self,data:dict):
        self.__multi = data

    def getMultiDefualtsetting(self)->dict:
        return {"timeanswer":5,"swin":3,"scloser":1,"rangenumb":5}

    def SaveSetting(self)->None:
        self.__endocode = json.JSONEncoder()
        self.__defulat = self.__endocode.encode(self.__mydict)
        with open(self.__path,"w+") as f:
            f.write(self.__defulat)
            f.close()

    def Save(self,data:dict):
        self.__endocode = json.JSONEncoder()
        self.__defulat = self.__endocode.encode(data)
        with open(self.__path,"w+") as f:
            f.write(self.__defulat)
            f.close()

class guisetting(QWidget):
    saveMulti = pyqtSignal(dict)
    checkboxes :List[QCheckBox]
    def __init__(self,setting:Setting,multi:bool=False) -> None:
        super().__init__()
        self.setObjectName("my")
        
        self.setWindowTitle("Setting Game")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        # setting
        self.__setting = setting
        self.__setting.loadSave() # new loading for sure
        self.__dataSetting = self.__setting.getSetting()
        self.setStyleSheet(self.css())
        # top pin
        self.pintop = QCheckBox()
        self.pintop.setText("Pin Top")
        self.pintop.setChecked(True)
        self.pintop.stateChanged.connect(self.__checkstateChange)
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
        self.__lineEdit.setObjectName("set")

        self.__lineEditdigit = QLineEdit(str(self.__dataSetting["digit"]))
        self.__lineEditdigit.editingFinished.connect(self.__lineeditdigitChangeAction)
        self.__lineEditdigit.setObjectName("set")
        
        self.__lineEditstep = QLineEdit(str(self.__dataSetting["step"]))
        self.__lineEditstep.editingFinished.connect(self.__lineeditstepChangeAction)
        self.__lineEditstep.setObjectName("set")

        self.__lineEdittimeofstep = QLineEdit(str(self.__dataSetting["timeofstep"]))
        self.__lineEdittimeofstep.editingFinished.connect(self.__lineedittimeofstepChangeAction)
        self.__lineEdittimeofstep.setObjectName("set")

        #ckeckbox
        self.checkboxes = []
        for opera in operation:
            checkbox = QCheckBox(opera.value)
            try:
                self.__dataSetting["operation"].index(opera.value)
                checkbox.setChecked(True)
                checkbox.setObjectName("set")
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
        self.__layoutcol.addWidget(self.pintop)
        self.__layoutcol.addLayout(self.__layoutrow1)
        self.__layoutcol.addLayout(self.__layoutrow2)
        self.__layoutcol.addLayout(self.__layoutrow3)
        self.__layoutcol.addLayout(self.__layoutrow4)
        self.__layoutcol.addLayout(self.__layoutrow5)
        self.__layoutcol.addLayout(self.__layoutrow)
        self.multiw=multi
        if self.multiw:
            self.MultiSetting()
            self.settingMulti = self.__setting.getSettingMulti()
        else:
            self.setMinimumHeight(300)
            self.setMinimumWidth(300)

        # add layout in widget
        self.setLayout(self.__layoutcol)
    def OnlyView(self):
        self.__savebutton.setVisible(False)
        self.__loaddefault.setVisible(False)
        self.pintop.setVisible(False)
        self.setDisabled(True)
    def __checkstateChange(self,e):
        if Qt.CheckState(e) == Qt.CheckState.Checked:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,True)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()
    def __savebuttonActionClick(self,e):
        if self.multiw:
            self.__setting.setMulti(self.settingMulti)
            self.__setting.updateMulti()
            self.saveMulti.emit(self.__setting.getSettingMulti())
        else:
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
        self.timeanswer.setText(str(5))
        self.scorewin.setText(str(3))
        self.scorecloser.setText(str(1))
        self.rangeofguess.setText(str(5))
        self.settingMulti = self.__setting.getMultiDefualtsetting()
        self.__setting.setMulti(self.settingMulti)
        self.__setting.SettingISDefualtSetting()
        self.__setting.updateMulti()
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
    
    def __rangeChange(self):
        try:
            print(self.rangeofguess.text(),293)
            self.settingMulti["rangenumb"] = int(self.rangeofguess.text())
        except:
            self.rangeofguess.setText("5")
    def __scloseChange(self):
        try:
           self.settingMulti["scloser"]= int(self.scorecloser.text())
        except:
            self.scorecloser.setText("1")
    def __swinChange(self):
        try:
            self.settingMulti["swin"]= int(self.scorewin.text())
        except:
            self.scorewin.setText("3")
    def __timeanswerChange(self):
        try:
            self.settingMulti["timeanswer"]= int(self.timeanswer.text())
        except:
            self.timeanswer.setText("5")
    def setALLSettingView(self,data:dict):
        data.pop("type")
        data.pop("action")
        self.__lineEdit.setText(str(data["match"]))
        self.__lineEditdigit.setText(str(data["digit"]))
        self.__lineEditstep.setText(str(data["step"]))
        self.__lineEdittimeofstep.setText(str(data["timeofstep"]))
        for x in self.checkboxes:
            if x.text() in data["operation"]:
               x.setChecked(True)
            else:
               x.setChecked(False)
        self.timeanswer.setText(str(data["timeanswer"]))
        self.scorewin.setText(str(data["swin"]))
        self.scorecloser.setText(str(data["scloser"]))
        self.rangeofguess.setText(str(data["rangenumb"]))

    
    def MultiSetting(self):
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("TimeofAnswer"))
        self.timeanswer = QLineEdit("5")
        row1.addWidget(self.timeanswer)
        self.timeanswer.editingFinished.connect(self.__timeanswerChange)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Score add win"))
        self.scorewin = QLineEdit("3")
        row2.addWidget(self.scorewin)
        self.scorewin.editingFinished.connect(self.__swinChange)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Score add closer"))
        self.scorecloser = QLineEdit("1")
        row3.addWidget(self.scorecloser)
        self.scorecloser.editingFinished.connect(self.__scloseChange)

        row4 =QHBoxLayout()
        row4.addWidget(QLabel("Range of closer guess number"))
        self.rangeofguess = QLineEdit("5")
        self.rangeofguess.editingFinished.connect(self.__rangeChange)

        row4.addWidget(self.rangeofguess)
        self.__layoutcol.addLayout(row1)
        self.__layoutcol.addLayout(row2)
        self.__layoutcol.addLayout(row3)
        self.__layoutcol.addLayout(row4)

    def css(self)->str:
        cssdata = ""
        with open("setting.css","r") as f:
            cssdata = f.read()
            f.close()
        return cssdata