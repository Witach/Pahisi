from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

class Widgets(QWidget):
    numberOfPlayers = 2
    port = 6669
    startedPivot = False
    adress = '127.0.0.1'

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
     
        
        textVBox = self.createTextVBox('set IP:', 'set port:')

        splitter = self.createInteractBox(textVBox)
        #movie =  self.createLabelGif('client/resources/pachisi.gif',110)
        mainVerticalList = self.createMainVerticaLList(splitter,'client/resources/dice.png')

        self.setLayout(mainVerticalList)
        
    def createLabelGif(self,filename,speed):
        movie = self.loadFileIntoMovie(filename)
        movieScreen = self.makeLabelfitTheGif()
        self.addTheMovieOBjectToTheLabel(movie,speed,movieScreen)
        return movieScreen
        
    def loadFileIntoMovie(self,filename):
        movie = QMovie(filename, QByteArray(), self)

        movie.setScaledSize(QSize().scaled(400,400,Qt.KeepAspectRatio))
        return movie
        
    def makeLabelfitTheGif(self):
        movie_screen = QLabel()
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        
        movie_screen.setStyleSheet("QLabel {padding: 0px 0px 0px 0px;}")
        return movie_screen
        
    def addTheMovieOBjectToTheLabel(self, movie,speed,movie_screen):
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(speed)
        movie_screen.setMovie(movie)
        movie.start()
    
        

    def createMainVerticaLList(self, splitter,path):
        
        mainVerticalList = QVBoxLayout()
        mainVerticalList.setContentsMargins(25,40,25,40)
        mainVerticalList.setSpacing(12)
        
        mainVerticalList.addWidget(self.setImage(path))
        mainVerticalList.addLayout(splitter)
        mainVerticalList.addWidget(self.createStart(self.startGame,'Start'))
        #mainVerticalList.addStretch(10)
        return mainVerticalList
    def setImage(self,path):
        label = QLabel(self)
        Image = QImage(path)
        
        label.setPixmap(QPixmap.fromImage(Image.scaled(300,300)))
        label.setScaledContents(False)
        
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("QLabel {padding: 30px 30px 30px 30px;}")
        return label

    def createInteractBox(self, textVBox):
        interactVBox = QVBoxLayout()
        splitter = QHBoxLayout()
        
        splitter.addLayout(textVBox)
        splitter.addLayout(interactVBox)
        self.textBoxPort = QLineEdit(self)
        self.textBoxPort.setStyleSheet("QLineEdit {color: white;background-color:#151515;border-style: outset;border-radius: 10px;font-size: 15px;font-family: Arial;font-weight: bold;padding: 5px 5px 5px 5px;}")
        self.textBoxAdress = QLineEdit(self)
        self.textBoxAdress.setStyleSheet("QLineEdit {color: white;background-color:#151515;border-style: outset;border-radius: 10px;font-size: 15px;font-family: Arial;font-weight: bold;padding: 5px 5px 5px 5px;}")
        self.textBoxPort.setText(str(self.port))
        self.textBoxAdress.setText(str(self.adress))
        
        interactVBox.addWidget(self.textBoxAdress)
        interactVBox.addWidget(self.textBoxPort)
        
        return splitter

    def createPlayerHbox(self, buttonDicriment, buttonIncriment):
        playerHBox = QHBoxLayout()
        playerHBox.setAlignment(Qt.AlignLeft)
        for widget in [buttonDicriment, self.textBoxPlayers, buttonIncriment]:
            playerHBox.addWidget(widget)
        return playerHBox

    def createTextVBox(self, portText, playerText):
        textVBox = QVBoxLayout()
        l1 = QLabel(portText)
        l2 = QLabel(playerText)
        l1.setStyleSheet("QLabel {color: white;background-color:#151515;border-style: outset;border-radius: 10px;font-size: 15px;font-family: Arial;font-weight: bold;padding: 5px 5px 5px 5px;}")
        l2.setStyleSheet("QLabel {color: white;background-color:#151515;border-style: outset;border-radius: 10px;font-size: 15px;font-family: Arial;font-weight: bold;padding: 5px 5px 5px 5px;}")
        textVBox.addWidget(l1)
        textVBox.addWidget(l2)
        return textVBox

    def createButton(self, fun, icon, maxWidth=50, minWidth=25):
        button = QPushButton(icon)
        button.clicked.connect(fun)
        button.setMaximumWidth(maxWidth)
        button.setMinimumWidth(minWidth)
        return button
    def createStart(self, method, name):
        button = QPushButton(name)
       
        #button.setContentsMargins(10,30,30,30)
        button.setStyleSheet("QPushButton {font-size: 25px;color: white;background-color:#151515;border-style: outset;border-radius: 15px;font-family: Arial;padding: 10px 5px 10px 5px;}QPushButton:hover:!pressed {background-color: #2A2A2A;}")
        button.clicked.connect(method)
        return button
    def startGame(self):
        print('start!')
   

    

        
        

  
