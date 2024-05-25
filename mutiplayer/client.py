import socket
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget,QLabel,QPushButton,QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from mutiplayer.server import ServerWindow

class SocketServerisAlive(QThread):
    checkServerAlive = pyqtSignal(bool)
    def __init__(self, s):
        super().__init__()
        self.s = s
        self.running = True
    def run(self):
            print("checker runing")
            count = 0
            while self.running:
                try:
                    self.s.send(b"check")
                    self.checkServerAlive.emit(True)
                    count = 0
                except:
                    self.checkServerAlive.emit(False)
                    count+=1
                    if count ==10:
                        break
                QThread.sleep(5)
                    
    def stop(self):
        self.running=False
class SocketThread(QThread):
    message_received = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)
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
            self.message_received.emit("finding server")
            self.s.connect((self.host, self.port))
            self.connection_status_changed.emit(True)
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
            self.connection_status_changed.emit(False)
    def send(self,s):
        self.s.send(s)
    def stop(self):
        self.running = False
        self.s.close()
        self.connection_status_changed.emit(False)
    def getS(self):
        return self.s

class clientGui(QWidget):
    closeClient = pyqtSignal(bool)
    def __init__(self,host="localhost",port=3430,master=False):
        super().__init__()
        self.__master = master
        self.port=port
        self.host=host
        
        self.setWindowTitle('Connect Server')
        self.__title = QLabel("Mutiplayer")
        self.report = QLabel("")
        
        self.__listpeoplename = QLabel()
        self.__ready = QPushButton("Ready")
        self.__ready.setObjectName("mutiready")
        self.__butclose = QPushButton("Exit Room")
        self.__butclose.clicked.connect(self.closebuttonEvent)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.__title)
        layout2.addWidget(self.report)
        layout2.addWidget(self.__listpeoplename)
        layout2.addWidget(self.__ready)
        layout2.addWidget(self.__butclose)
        self.setLayout(layout2)
        if(self.__master):
            self.serverview = ServerWindow()
            self.serverview.show()
            self.serverview.ServerIsStarted.connect(self.__ConnectServer)
        else:
            self.__ConnectServer(False)

    def __ConnectServer(self,b):
        if b:
            self.port = self.serverview.getPort()
        self.socket_thread = SocketThread(self.host,self.port)
        self.socket_thread.message_received.connect(self.display_message)
        self.socket_thread.connection_status_changed.connect(self.update_connection_status)
        self.socket_thread.client_connected.connect(self.notdata)
        self.socket_thread.start()
        self.checker = SocketServerisAlive(self.socket_thread.getS())
        self.checker.checkServerAlive.connect(self.__dochecker)
    @pyqtSlot(str)
    def display_message(self, message):
        self.report.setText(message)
    @pyqtSlot(socket.socket)
    def notdata(self,b):
        self.checker.start()
    @pyqtSlot(bool)
    def update_connection_status(self, connected):
        if connected:
            self.report.setText("Connected to the server.")
        else:
            self.report.setText("donnected to the server.")
    def closebuttonEvent(self):
        self.socket_thread.stop()
        print("ss")
        self.closeClient.emit(True)
    def closeEvent(self, event):
        self.socket_thread.stop()
        super().closeEvent(event)
    def __dochecker(self, b: bool):
        if not b:
            self.report.setText("donnected to the server.")
            
        print(b)
            