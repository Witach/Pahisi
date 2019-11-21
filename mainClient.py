
from client.clientGUI import MyMainWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    
    app.setStyleSheet('QMainWindow{background-color:orange;border: 1px solid black;}')
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec_())


