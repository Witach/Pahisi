from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Widgets(QWidget):
    numberOfPlayers = 2
    port = 6669

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.iniTextBoxOfPlayers()

        textVBox = self.createTextVBox('set port:', 'set players:')

        buttonDicriment = self.createButton(self.dicriment, '◄')
        buttonIncriment = self.createButton(self.increment, '►')
        playerHBox = self.createPlayerHbox(buttonDicriment, buttonIncriment)

        splitter = self.createInteractBox(textVBox, playerHBox)

        mainVerticalList = self.createMainVerticaLList(splitter)

        self.setLayout(mainVerticalList)

    def createMainVerticaLList(self, splitter):
        textBoxLogs = QTextEdit(self)
        textBoxLogs.setReadOnly(True)
        mainVerticalList = QVBoxLayout()
        mainVerticalList.addLayout(splitter)
        mainVerticalList.addWidget(QPushButton('Start'))
        mainVerticalList.addWidget(textBoxLogs)
        return mainVerticalList

    def createInteractBox(self, textVBox, playerHBox):
        interactVBox = QVBoxLayout()
        splitter = QHBoxLayout()
        splitter.addLayout(textVBox)
        splitter.addLayout(interactVBox)
        textBoxPort = QLineEdit(self)
        textBoxPort.setText(str(self.port))
        interactVBox.addWidget(textBoxPort)
        interactVBox.addLayout(playerHBox)
        return splitter

    def createPlayerHbox(self, buttonDicriment, buttonIncriment):
        playerHBox = QHBoxLayout()
        playerHBox.setAlignment(Qt.AlignLeft)
        for widget in [buttonDicriment, self.textBoxPlayers, buttonIncriment]:
            playerHBox.addWidget(widget)
        return playerHBox

    def createTextVBox(self, portText, playerText):
        textVBox = QVBoxLayout()
        for widget in [QLabel(portText), QLabel(playerText)]:
            textVBox.addWidget(widget)
        return textVBox

    def createButton(self, fun, icon, maxWidth=50, minWidth=25):
        button = QPushButton(icon)
        button.clicked.connect(fun)
        button.setMaximumWidth(maxWidth)
        button.setMinimumWidth(minWidth)
        return button

    def iniTextBoxOfPlayers(self):
        self.textBoxPlayers = QTextEdit(self)
        self.textBoxPlayers.setReadOnly(True)
        self.textBoxPlayers.setMinimumHeight(10)
        self.textBoxPlayers.setMaximumHeight(25)
        self.textBoxPlayers.setMaximumWidth(30)
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))

    def fileTreeBuilder(self):
        tree = QTreeView()
        tree.setModel(self.model)
        tree.setAnimated(True)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)
        tree.resize(640, 480)
        return tree

    def increment(self):
        if self.numberOfPlayers < 4:
            self.numberOfPlayers += 1
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))

    def dicriment(self):
        if self.numberOfPlayers > 2:
            self.numberOfPlayers -= 1
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))
