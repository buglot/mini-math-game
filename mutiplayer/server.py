import socket
import select
from typing import List
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication,QCheckBox, QMainWindow, QTextEdit, QVBoxLayout, QWidget,QLabel,QHBoxLayout
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread,Qt
from mutiplayer.typeMassegeSocket import TypeMassnge
import sys
class ClientHandler(QThread):
    message_received = pyqtSignal(str)
    closed_by_the_remote = pyqtSignal(QThread)
    __data:dict
    def __init__(self):
        super().__init__()
        self.Type = TypeMassnge()
        self.Type.SystemCallActionEven.connect(self.register)
        self.running = True
    def register(self,data:dict):
        if TypeMassnge.ActionSystemCall(data["action"]) == TypeMassnge.ActionSystemCall.JOIN:
            self.__data = data
    def deleteList(self)->list:
        if self.__data:
            self.__data["action"] = TypeMassnge.ActionSystemCall.EXIT.value
            return self.__data
        return None
    def setC(self,client_socket:socket.socket):
        self.client_socket =client_socket
    def run(self):
        d=0
        with self.client_socket:
            while self.running:
                try:
                    data1= self.client_socket.recv(1024)
                    if not data1:
                        break
                    message = data1.decode('utf-8')
                    self.Type.isType(message)
                    self.message_received.emit(message)
                except Exception as E:
                    print("error:28 ",E)
                    self.closed_by_the_remote.emit(self)
                    self.stop()
    def send(self,msg:bytes):
        self.client_socket.send(msg)
    def stop(self):
        self.running = False
        self.client_socket.close()
        print("stop")
        self.quit()

class ServerWindow(QWidget):
    ServerIsStarted = pyqtSignal(bool)
    serverlist:List[ClientHandler]
    def __init__(self):
        super().__init__()
        self.listpeople = []
        self.setWindowTitle('Socket Server with PyQt6 QThread')
        self.l = QLabel("SERVER")
        self.l.setObjectName("OpenServer")
        self.port = QLabel()
        self.v = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.chat =QTextEdit()
        self.gameLog = QTextEdit()
        self.host = QLabel(f"{socket.gethostbyname(socket.gethostname())}:")
        self.port.setObjectName("Lurl")
        self.host.setObjectName("Lurl")
        self.checkbox = QCheckBox()
        self.checkbox.setText("Pin Top")
        self.checkbox.setChecked(True)
        self.checkbox.checkStateChanged.connect(self.checkboxAction)
        self.host.setToolTip("Click for Copy")
        self.port.setToolTip("Click for Copy")
        self.host.mouseReleaseEvent = self.copy
        self.port.mouseReleaseEvent = self.copy
        row1 = QHBoxLayout()
        row1.addWidget(self.l)
        row1.addWidget(self.checkbox)
        self.r = QHBoxLayout()
        self.r.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.r.addWidget(self.host)
        self.r.addWidget(self.port)
        self.v.addLayout(row1)
        self.v.addLayout(self.r)
        self.v.addWidget(QLabel("Game LOG"))
        self.v.addWidget(self.gameLog)
        self.v.addWidget(QLabel("Chat"))
        self.v.addWidget(self.chat)
        self.v.addWidget(QLabel("System Call"))
        self.v.addWidget(self.text_edit)
        self.setLayout(self.v)
        self.setStyleSheet(self.css())
        self.TypeM = TypeMassnge()
        self.TypeM.SystemCallActionEven.connect(self.readall)
        self.TypeM.ChatActionEven.connect(self.__chatAction)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,True)
        self.serverlist =[]
    def startServer(self):
        self.server_thread = ServerThread(host=socket.gethostbyname(socket.gethostname()))
        self.server_thread.client_connected.connect(self.handle_client_connection)
        self.server_thread.nowPort.connect(self.newPort)
        self.server_thread.finished.connect(self.server_thread_ended)
        self.server_thread.start()
    def __chatAction(self,data:dict):
        self.chat.append(data["name"]+":"+data["msg"])
        self.sendsAll(self.TypeM.encode(data=data).encode())
    def checkboxAction(self,e):
        if e== Qt.CheckState.Checked:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,True)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()
    def css(self):
        s=""
        with open("server.css") as f:
                s = f.read()
                f.close()
        return s
    def getHost(self):
        return socket.gethostbyname(socket.gethostname())
    def sendsAll(self,msg):
        for x in self.serverlist:
            x.send(msg)
    def copy(self,e):
         QGuiApplication.clipboard().setText(self.host.text()+self.port.text())
    @pyqtSlot(dict)
    def readall(self,data:dict):
        match TypeMassnge.ActionSystemCall(data["action"]):
            case TypeMassnge.ActionSystemCall.PING:
                self.text_edit.append(data["name"]+": PING")
            case TypeMassnge.ActionSystemCall.KICK:
                self.text_edit.append(data["name"]+": was KICKED by Master")
            case TypeMassnge.ActionSystemCall.EXIT:
                self.text_edit.append(data["name"]+": EXIT")
                self.listpeople.remove([data["name"],data["uuid"]])
                print("Server 130",self.listpeople)
                data = {"type":TypeMassnge.Type.SYSTEMCALL.value,
                        "action":TypeMassnge.ActionSystemCall.GETLISTPEOPLE.value,
                        "nPeople":len(self.listpeople),
                        "data":self.listpeople}
                self.sendsAll(self.TypeM.encode(data).encode())
            case TypeMassnge.ActionSystemCall.JOIN:
                self.listpeople.append([data["name"],data["uuid"]])
                self.text_edit.append(data["name"]+": JOIN")
            case TypeMassnge.ActionSystemCall.CALL_LISTPEOPLE:
                data = {"type":TypeMassnge.Type.SYSTEMCALL.value,
                        "action":TypeMassnge.ActionSystemCall.GETLISTPEOPLE.value,
                        "nPeople":len(self.listpeople),
                        "data":self.listpeople}
                self.sendsAll(self.TypeM.encode(data).encode())
    def getPort(self)->int:
        return int(self.port.text())
    @pyqtSlot(int)
    def newPort(self,port:int):
        self.port.setText(str(port))
        self.ServerIsStarted.emit(True)
    
    @pyqtSlot(socket.socket)
    def handle_client_connection(self, client_socket):
        self.handler = ClientHandler()
        self.handler.setC(client_socket)
        self.handler.message_received.connect(self.display_message)
        self.handler.closed_by_the_remote.connect(self.__closeClientConnect)
        self.serverlist.append(self.handler)
        self.handler.start()
    def __closeClientConnect(self,f:ClientHandler):
        print(f,self.serverlist)
        try:
            self.serverlist.remove(f)
            self.TypeM.isType(self.TypeM.encode(f.deleteList()))
        except ValueError as E:
            print("Error ValueError 170",E)
        

    @pyqtSlot(str)
    def display_message(self, message):
        self.TypeM.isType(message)
    def closeEvent(self, event):
        if self.handler:
            self.handler.stop()
        self.server_thread.stop()
        super().closeEvent(event)
    def server_thread_ended(self):
        print("server closed")
class ServerThread(QThread):
    client_connected = pyqtSignal(socket.socket)
    nowPort = pyqtSignal(int)
    def __init__(self,host="localhost",port=3430):
        super().__init__()
        self.running = True
        self.host = host
        self.port = port
    def run(self):
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.host, self.port))
        except:
            for x in range(10):
                self.port+=1
                try:
                    self.server_socket.bind((self.host, self.port))
                    break
                except:
                    pass
        self.server_socket.listen(5)
        self.nowPort.emit(self.port)
        while self.running:
            try:
                self.client_socket, addr = self.server_socket.accept()
                self.client_connected.emit(self.client_socket)
            except Exception as e:
                print("Error accepting connection:", e)
                break
    def stop(self):
        self.running = False
        self.server_socket.close()
        self.quit()
        

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    gui = ServerWindow()
    gui.show()
    sys.exit(app.exec())