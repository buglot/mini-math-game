import uuid
import json
import enum
import os
import random
from PyQt6.QtCore import QObject,pyqtSignal
class MassngeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class TypeMassnge(QObject):
    class Type(enum.Enum):
        CHAT = 1
        GAMECONTROLL = 2
        SYSTEMCALL = 3
    class ActionSystemCall(enum.Enum):
        PING = "PING"
        KICK = 0
        CALL_LISTPEOPLE = 1
        GETLISTPEOPLE = 2
        EXIT = 3
        JOIN = 4
    ChatActionEven = pyqtSignal(dict)
    GameControllActionEven = pyqtSignal(dict)
    SystemCallActionEven = pyqtSignal(dict)
    def __init__(self) -> None:
        super().__init__()
        self.__encode = json.JSONEncoder()
        self.__decode = json.JSONDecoder()
        if self.isUUID():
            self.__UUID()
        else:
            self.GenUUID()
            self.__UUID()

    def encode(self,data:dict)->str:
        return self.__encode.encode(data)
    def __UUID(self):
        my = open("uuid.id")
        self.__uuid= my.read()
        my.close()
    def UUID(self):
        return self.__uuid
    def isType(self,b:str):
        try:
            if len(b.split("{")[1:])>1:
                raise MassngeError("Error")
            data= self.__decode.decode(b)
            self.__checkType(data)
        except MassngeError:
            for x in b.split("{")[1:]:
                self.__checkType(self.__decode.decode("{"+x))
        except Exception as e:
            print("isTypeError",e)
    def __checkType(self,data:dict):
        match TypeMassnge.Type(data["type"]):
            case TypeMassnge.Type.CHAT:
                self.ChatActionEven.emit(data)
            case TypeMassnge.Type.GAMECONTROLL:
                self.GameControllActionEven.emit(data)
            case TypeMassnge.Type.SYSTEMCALL:
                self.SystemCallActionEven.emit(data)
    def GenUUID(self):
        data = random.choice(range(1,300))
        with open("uuid.id","w") as f:
            f.write(str(uuid.uuid1())+"-"+str(data))
            f.close()
    def isUUID(self)->bool:
        if os.path.exists("uuid.id"):
            return True
        return False

