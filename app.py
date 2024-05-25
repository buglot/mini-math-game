import sys
from PyQt6.QtWidgets import QApplication
from setting import Setting
from game import GameWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    setting = Setting()
    gui = GameWindow(set=setting)
    gui.show()
    sys.exit(app.exec())