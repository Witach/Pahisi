import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from win32api import GetSystemMetrics

import random
import time

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
    milieusPositionsCoordinates = [[24,370],[98,370],[182,370],[264,370],[366,366],[366,278],
                                   [366,192],[366,104],[366,28],[456,24],[544,22],[544,102],
                                   [544,184],[544,266],[544,362],[622,366],[708,366],[796,366],
                                   [880,366],[880,456],[880,542],[798,544],[710,544],[622,544],
                                   [544,544],[544,626],[544,708],[544,790],[544,886],[458,886],
                                   [368,882],[368,800],[368,714],[368,626],[368,544],[266,540],
                                   [182,540],[100,540],[26,540],[26,460]]
    
    winnerPositionsCoordinates = [[[106,456],[194,458],[282,458],[364,456]],
                                  [[452,108],[452,194],[452,280],[452,362]],
                                  [[798,454],[716,454],[628,454],[542,454]],
                                  [[454,802],[454,716],[454,628],[454,546]]]
    
    dicesPositionCoordinates = [[238,235],[667,233],[668,672],[239,669]]
    #lists of labels
    redPawnsStartingPosiotions = []
    bluePawnsStartingPosiotions = []
    greenPawnsStartingPosiotions = []
    yellowPawnsStartingPosiotions = []
    
    starterPositions = []
    #surroundings layer
    milieusPositions = []
    #winning Posistions
    redWinningPositions = []
    blueWinningPositions = []
    greenWinningPositions = []
    yellowWinningPositions = []
    #dice
    dicePositions = []
    #current posistions of pawns
    #list of label that pawn have
    redPawns = []
    bluePawns = []
    greenPawns = []
    yellowPawns = []
    
    
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
        
        for n in range(10):
            QApplication.processEvents()
            time.sleep(0.1)
        #if statement needed, when server collected all players (OK TRUE)
    #def moveOnScreen(self):
        
        
    def init(self,path="resources/table.png"):
        
        self.initScreenSize()
        self.initBackground(993,path)
        self.setAllPawnsPosiotions()
        
        self.setPawnsImages()
        self.setDicesImages()
        
    def setAllPawnsPosiotions(self):
        self.createPawnPosiotions(self.redPawnsStartingPositionsCoordinates,self.redPawnsStartingPosiotions)
        self.createPawnPosiotions(self.bluePawnsStartingPositionsCoordinates,self.bluePawnsStartingPosiotions)
        self.createPawnPosiotions(self.greenPawnsStartingPositionsCoordinates,self.greenPawnsStartingPosiotions)
        self.createPawnPosiotions(self.yellowPawnsStartingPositionsCoordinates,self.yellowPawnsStartingPosiotions)
        self.createPawnPosiotions(self.starterPositionsCoordinates,self.starterPositions)
        self.createPawnPosiotions(self.milieusPositionsCoordinates,self.milieusPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[0],self.redWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[1],self.blueWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[2],self.greenWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[3],self.yellowWinningPositions)
        self.createPawnPosiotions(self.dicesPositionCoordinates,self.dicePositions)
        ##TODO REST OF POSISTIONS
        
    def setPawnsImages(self):
        self.redPawnImage = self.createPawn('resources/redPawn.png')
        self.bluePawnImage = self.createPawn('resources/bluePawn.png')
        self.greenPawnImage = self.createPawn('resources/greenPawn.png')
        self.yellowPawnImage = self.createPawn('resources/yellowPawn.png')
    def setDicesImages(self):
        self.diceImage = []
        path = 'resources/k'
        for i in range(1,6):
            Image = self.createDice('resources/k'+ str(i) +'.png')
            self.diceImage.append(Image)
        
    def gameStart(self):
        #asking server about players roles and quantity
        self.setPawnsOnStartingPosiotions()
        #nasluchuje server czeka na zmiany 
        """
            server przydziela kolejke kazdemu graczowi wtedy client czeka
            az server odda tę kolejke mu. Gdy mu odda kolejke wtedy on losuje liczbe lub 
            server oddajac mu kolejke wysyla mu liczbe oraz wszystkim innym gracza (tak lepiej chyba)
            
            
        """
        self.movePawn(self.redPawns[0],self.milieusPositions[0])
        
        
        #self.movePawn(self.milieusPositions[0],self.redPawnsStartingPosiotions[0],self.redPawnImage)
        #rest of game
    def movePawn(self,pawn,destinationPosition):
        
        pawn.getCurrentPosition().setVisible(False)
        pawn.setCurrentPosition(destinationPosition)
        self.setPawnOnPosition(pawn)
        
   
        
        
        
        
    def roleTheDice(self):
        #1 - 6 - 1
        return random.randint(0,6) - 1
    
        
        
    def setPawnsOnStartingPosiotions(self):
        rolesArray = self.getPlayersRoles()
        for i in rolesArray:
            j = 0
            if i == self.red:
                for i in self.redPawnsStartingPosiotions:
                    self.redPawns.append(Pawn(i,self.redPawnImage,'red'))
                    self.setPawnOnPosition(self.redPawns[j])
                    j+=1
            elif i == self.blue:
                for i in self.bluePawnsStartingPosiotions:
                    self.bluePawns.append(Pawn(i,self.bluePawnImage,'blue'))
                    self.setPawnOnPosition(self.bluePawns[j])
                    j+=1
            elif i == self.green:
                for i in self.greenPawnsStartingPosiotions:
                    self.greenPawns.append(Pawn(i,self.greenPawnImage,'green'))
                    self.setPawnOnPosition(self.greenPawns[j])
                    j+=1
            elif i == self.yellow:
                for i in self.yellowPawnsStartingPosiotions:
                    self.yellowPawns.append(Pawn(i,self.yellowPawnImage,'yellow'))
                    self.setPawnOnPosition(self.yellowPawns[j])
                    j+=1     
    
    def createPawnPosiotions(self,coordinates,posiotions):
       
        j = 0
        for i in coordinates:
            posiotions.append(QLabel(self))
            posiotions[j].move(i[0], i[1])
            j+=1
            
    def setPawnOnPosition(self,pawn): 
        """
            Position is a label 
            pawn is scaled picture 
        """
        pawn.getCurrentPosition().setPixmap(QPixmap.fromImage(pawn.getColor()))
        pawn.getCurrentPosition().setScaledContents(False)
        pawn.getCurrentPosition().setVisible(True)
        pawn.getCurrentPosition().setAlignment(Qt.AlignCenter)
        pawn.getCurrentPosition().setStyleSheet('QLabel{border: 1px solid white;border-style: outset;border-radius: 37px;}QLabel:hover{border: 17px solid '+pawn.getColorName() +';border-radius: 37px;}')
        
    def createDice(self,path):
        Image = QImage(path)
        Image = Image.scaled(100,100)
        return Image
        
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
        tempArray = [1,2,3,4]
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
class Pawn():
    def __init__(self,posistion,color,colorName):
        self.currentPosition = posistion
        self.pawnColor = color
        self.colorName = colorName
    def getCurrentPosition(self):
        return self.currentPosition
    def getColor(self):
        return self.pawnColor
    def setCurrentPosition(self,position):
        self.currentPosition = position
    def getColorName(self):
        return self.colorName
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    #app.setStyleSheet('QWidget{background-color:black}')
    oMainwindow = GamePanel(app)
    sys.exit(app.exec_())
    
    

   

