from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

class Widgets(QWidget):
    numberOfPlayers = 2
    port = 6669
    startedPivot = False

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
        movie =  self.createLabelGif('server/resources/server.gif',100)
        mainVerticalList = self.createMainVerticaLList(splitter,movie)

        self.setLayout(mainVerticalList)
        
    def createLabelGif(self,filename,speed):
        movie = self.loadFileIntoMovie(filename)
        movieScreen = self.makeLabelfitTheGif()
        self.addTheMovieOBjectToTheLabel(movie,speed,movieScreen)
        return movieScreen
        
    def loadFileIntoMovie(self,filename):
        movie = QMovie(filename, QByteArray(), self)

        movie.setScaledSize(QSize().scaled(200,200,Qt.KeepAspectRatio))
        return movie
        
    def makeLabelfitTheGif(self):
        movie_screen = QLabel()
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        
        movie_screen.setStyleSheet("QLabel {padding: 20px 0px 20px 0px;}")
        return movie_screen
        
    def addTheMovieOBjectToTheLabel(self, movie,speed,movie_screen):
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(speed)
        movie_screen.setMovie(movie)
        movie.start()
    
        

    def createMainVerticaLList(self, splitter,movie):
        self.textBoxLogs = QTextEdit(self)
        self.textBoxLogs.setReadOnly(True)
        mainVerticalList = QVBoxLayout()
        mainVerticalList.addWidget(movie)
        mainVerticalList.addLayout(splitter)
        mainVerticalList.addWidget(self.createStart(self.startServer,'Start'))
        mainVerticalList.addWidget(self.textBoxLogs)
        return mainVerticalList

    def createInteractBox(self, textVBox, playerHBox):
        interactVBox = QVBoxLayout()
        splitter = QHBoxLayout()
        splitter.addLayout(textVBox)
        splitter.addLayout(interactVBox)
        self.textBoxPort = QLineEdit(self)
        self.textBoxPort.setText(str(self.port))
        interactVBox.addWidget(self.textBoxPort)
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
    def createStart(self, method, name):
        button = QPushButton(name)
        button.clicked.connect(method)
        return button

    def iniTextBoxOfPlayers(self):
        self.textBoxPlayers = QTextEdit(self)
        self.textBoxPlayers.setReadOnly(True)
        self.textBoxPlayers.setMinimumHeight(10)
        self.textBoxPlayers.setMaximumHeight(25)
        self.textBoxPlayers.setMaximumWidth(30)
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))

    
    def startServer(self):
        if not self.startedPivot:
            self.textBoxLogs.setText('Server service started at ' + str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
            self.textBoxLogs.append('Server is started at port = ' + str(self.textBoxPort.text()))
            self.textBoxLogs.append('number of players = ' + str(self.numberOfPlayers))
            self.startedPivot = True
        
        

    def increment(self):
        if self.numberOfPlayers < 4:
            self.numberOfPlayers += 1
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))

    def dicriment(self):
        if self.numberOfPlayers > 2:
            self.numberOfPlayers -= 1
        self.textBoxPlayers.setText('  ' + str(self.numberOfPlayers))
