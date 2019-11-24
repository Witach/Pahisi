import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from win32api import GetSystemMetrics
import time
import threading
import math


class GamePanel(QWidget):
    port = 6669
    connected = True
    ipAdress = '127.0.0.1'
    role = 1 # colour of client
    
    red = 1
    blue = 2
    green = 3
    yellow= 4
    #Coordinates
    redPawnsStartingPositionsCoordinates = [[22,26],[110,24],[110,104],[22,108]]
    bluePawnsStartingPositionsCoordinates = [[788,22],[880,22],[880,102],[790,104]]
    greenPawnsStartingPositionsCoordinates = [[880,798],[880 ,892],[792 ,890],[792 ,800]]
    yellowPawnsStartingPositionsCoordinates = [[108 ,888],[24,890],[22,794],[110,794]]
    
    starterPositionsCoordinates = [[24,370],[544,22],[880,544],[366,882]]
    milieusPositions = [[24,370],[98,370],[182,370],[264,370],[366,366],[366,278],
                        [366,192],[366,104],[366,28],[456,24],[544,22],[544,102],
                        [544,184],[544,266],[544,362],[622,366],[708,366],[796,366],
                        [880,366],[880,456],[880,542],[798,544],[710,544],[622,544],
                        [544,544],[544,626],[544,708],[544,790],[544,886],[458,886],
                        [368,882],[368,800],[368,714],[368,626],[368,544],[266,540],
                        [182,540],[100,540],[26,540],[26,460]]
    #lists of labels
    redPawnsStartingPosiotions = []
    bluePawnsStartingPosiotions = []
    greenPawnsStartingPosiotions = []
    yellowPawnsStartingPosiotions = []
    
    starterPositions = []
    #surroundings layer
    milieusPositions = []
    winnerPositions = [[]]
    
    
    ##place for more positions
    
    def __init__(self,parent,ipAdress = '127.0.0.1',port = 6669):
       super().__init__()
       
       self.port = port
       self.ipAdress = ipAdress
       ##GIF WAITING staff
       
       
       self.initScreenSize()
       self.initBackground(993,'resources/wait.jpg')
       
       
       self.show()
       self.waitForPlayers()
       self.init()
       self.gameStart()
      
       
       
    
    
       
    
        
    def waitForPlayers(self):
        
        for n in range(20):
            QApplication.processEvents()
            time.sleep(0.1)
        #if statement needed, when server collected all players (OK TRUE)
        
        
    def init(self,path="resources/table.png"):
        
       self.initScreenSize()
       self.initBackground(993,path)
       self.setAllPawnsPosiotions()
       self.setPawnsImages()
    
    def setAllPawnsPosiotions(self):
        self.createPawnPosiotions(self.redPawnsStartingPositionsCoordinates,self.redPawnsStartingPosiotions)
        self.createPawnPosiotions(self.bluePawnsStartingPositionsCoordinates,self.bluePawnsStartingPosiotions)
        self.createPawnPosiotions(self.greenPawnsStartingPositionsCoordinates,self.greenPawnsStartingPosiotions)
        self.createPawnPosiotions(self.yellowPawnsStartingPositionsCoordinates,self.yellowPawnsStartingPosiotions)
        
        
        ##TODO REST OF POSISTIONS
        
    def setPawnsImages(self):
        self.redPawnImage = self.createPawn('resources/redPawn.png')
        self.bluePawnImage = self.createPawn('resources/bluePawn.png')
        self.greenPawnImage = self.createPawn('resources/greenPawn.png')
        self.yellowPawnImage = self.createPawn('resources/yellowPawn.png')
        
    def gameStart(self):
        #asking server about players roles and quantity
        self.setPawnsOnStartingPosiotions()
        #rest of game
        
        
        
        
        
    def setPawnsOnStartingPosiotions(self):
        rolesArray = self.getPlayersRoles()
        for i in rolesArray:
            if i == self.red:
                for i in self.redPawnsStartingPosiotions:
                    self.setPawnOnPosition(i,self.redPawnImage)
            if i == self.blue:
                for i in self.bluePawnsStartingPosiotions:
                    self.setPawnOnPosition(i,self.bluePawnImage)
            if i == self.green:
                for i in self.greenPawnsStartingPosiotions:
                    self.setPawnOnPosition(i,self.greenPawnImage)
            if i == self.yellow:
                for i in self.yellowPawnsStartingPosiotions:
                    self.setPawnOnPosition(i,self.yellowPawnImage)      
    
    def createPawnPosiotions(self,coordinates,posiotions):
       
        j = 0
        for i in coordinates:
            posiotions.append(QLabel(self))
            posiotions[j].move(i[0], i[1])
            j+=1
            
    def setPawnOnPosition(self,position,pawn): 
        """
            Position is a label 
            pawn is scaled picture 
        """
        position.setPixmap(QPixmap.fromImage(pawn))
        position.setScaledContents(False)
        position.setVisible(True)
        position.setAlignment(Qt.AlignCenter)
        
    
        
    def createPawn(self,path):
        Image = QImage(path)
        Image = Image.scaled(75,75)
        return Image
    
    def getPlayersRoles(self):
        """
            bierze od servera kolory innych graczy
            1 - czerwony
            2 - niebieski
            3 - zielony
            4 - zolty
            moglyby to byc enum ale dzialaloby to tak samo plus nie chce mi sie tego ogarniac w pythonie XD
        """ 
        tempArray = [1,2,3]
        return tempArray
    
        
    """
    def createImage(self,path):
        label = QLabel(self)
        Image = QImage(path)
        
        label.setPixmap(QPixmap.fromImage(Image.scaled(75,75)))
        label.setScaledContents(False)
        label.setVisible(False)
        
        label.setAlignment(Qt.AlignCenter)
    
        
    
        return label   
    """
    #Screen Settings   
    def initScreenSize(self):
       
       self.move(993/2,0)
       self.resize(993,993)
       self.setFixedSize(self.size())
       return 993
   
    def initBackground(self,screenWidth,path):
        oImage = QImage(path)
        sImage = oImage.scaled(QSize(screenWidth,screenWidth))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
   
    

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    #app.setStyleSheet('QWidget{background-color:black}')
    oMainwindow = GamePanel(app)
    sys.exit(app.exec_())
    
    

   

