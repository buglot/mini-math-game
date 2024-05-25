import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,QLabel
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread
import sys
class ClientHandler(QThread):
    message_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.running = True
    def setC(self,client_socket:socket.socket):
        self.client_socket =client_socket
    def run(self):
        d=0
        with self.client_socket:
            while self.running:
                try:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    self.message_received.emit(message)
                except Exception as E:
                    print(E)
    
    def stop(self):
        self.running = False
        
        self.client_socket.close()
        print("stop")
        self.quit()

class ServerWindow(QWidget):
    ServerIsStarted = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Socket Server with PyQt6 QThread')
        self.l = QLabel("SEVER")
        self.port = QLabel()
        self.v = QVBoxLayout()
        self.v.addWidget(self.l)
        self.text_edit = QTextEdit()
        self.v.addWidget(self.text_edit)
        self.v.addWidget(self.port)
        self.setLayout(self.v)
        self.server_thread = ServerThread()
        self.server_thread.client_connected.connect(self.handle_client_connection)
        self.server_thread.nowPort.connect(self.newPort)
        self.server_thread.finished.connect(self.server_thread_ended)
        self.server_thread.start()
        self.handler = ClientHandler()
    
    def getPort(self)->int:
        return int(self.port.text())
    @pyqtSlot(int)
    def newPort(self,port:int):
        self.port.setText(str(port))
        self.ServerIsStarted.emit(True)
        print(2)
    @pyqtSlot(socket.socket)
    def handle_client_connection(self, client_socket):
       
        self.handler.setC(client_socket)
        self.handler.message_received.connect(self.display_message)
        self.handler.start()
    @pyqtSlot(str)
    def display_message(self, message):
        self.text_edit.append(message)
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
                client_socket, addr = self.server_socket.accept()
                print(addr)
                self.client_connected.emit(client_socket)
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