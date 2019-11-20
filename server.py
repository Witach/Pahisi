# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:51:13 2019

@author: Artur 
"""
import sys
from PyQt5.QtWidgets import QMainWindow,QAbstractButton, QApplication, QPushButton, QAction, QFileSystemModel,QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,QTextEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('server.png'))
        self.title = 'Mensch ärgere Dich nicht'
        self.left = 200
        self.top = 40
        self.width = 350
        self.height = 400
        self.widgets = Widgets()
        
        self.setCentralWidget(self.widgets)
        
        self.initUIMainWindow()

    def initUIMainWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.move(1920 / 2 - self.height, 1080 / 2 -400)
        
        



class Widgets(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def fileTreeBuilder(self):
        tree = QTreeView()
        tree.setModel(self.model)
        tree.setAnimated(True)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)
        tree.resize(640, 480)
        return tree

    
        
    

    def initUI(self):
        mainVerticalList = QVBoxLayout()
        labelport = QLabel('set port:')
        labelplayers = QLabel('set players:')
        
        textBoxPort = QLineEdit(self)
        
        
        
        textBoxPlayers = QTextEdit(self)
        textBoxPlayers.setReadOnly(True)
        textBoxPlayers.setMinimumHeight(10)
        textBoxPlayers.setMaximumHeight(25)
        textBoxPlayers.setMaximumWidth(30)
        
        textBoxLogs = QTextEdit(self)
        textBoxLogs.setReadOnly(True)
        
        buttonDicriment = QPushButton('◄')
        buttonIncriment = QPushButton('►')
        buttonDicriment.setMaximumWidth(50)
        buttonDicriment.setMinimumWidth(25)
        buttonIncriment.setMaximumWidth(50)
        buttonIncriment.setMinimumWidth(25)
        buttonStart = QPushButton('Start')
        
        
        
        splitter = QHBoxLayout()
        textVBox = QVBoxLayout()
        interactVBox = QVBoxLayout()
        
        splitter.addLayout(textVBox)
        splitter.addLayout(interactVBox)
        
        textVBox.addWidget(labelport)
        textVBox.addWidget(labelplayers)
        
        playerHBox = QHBoxLayout()
        playerHBox.setAlignment(Qt.AlignLeft)
        playerHBox.addWidget(buttonDicriment)
        playerHBox.addWidget(textBoxPlayers)
        playerHBox.addWidget(buttonIncriment)
        
        interactVBox.addWidget(textBoxPort)
        interactVBox.addLayout(playerHBox)
        
        mainVerticalList.addLayout(splitter)
        mainVerticalList.addWidget(buttonStart)
        mainVerticalList.addWidget(textBoxLogs)
        
        
        
        self.setLayout(mainVerticalList)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec_())

