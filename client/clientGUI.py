
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .widgets import Widgets
import math

class MyMainWindow(QMainWindow):

    title = 'Mensch ärgere Dich nicht'
    left = 200
    top = 40
    width = 350
    height = 500
    screenHeight = 1080
    screenWidth = 1920

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowIcon(QIcon('client/resources/dice.png'))
        self.widgets = Widgets(self)
        self.setCentralWidget(self.widgets)
        self.initUIMainWindow()
        

    def initUIMainWindow(self):
        self.setWindowTitle(self.title)
        
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.move(
            math.floor(self.screenWidth / 2 - self.height),
            math.floor(self.screenHeight / 2 -400)
        )
        
