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
    redPawnsStartingPosition = [[22,26],[110,24],[110,104],[22,108]]
    bluePawnsStartingPosition = [[788,22],[880,22],[880,102],[790,104]]
    greenPawnsStartingPosition = [[880,798],[880 ,892],[792 ,890],[792 ,800]]
    yellowPawnsStartingPosition = [[108 ,888],[24,890],[22,794],[110,794]]
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
       self.close()#bardzo wazne
       self.init()
       self.show()
       
       
       
    
       
    def waitForPlayers(self):
        
        for n in range(1):
            QApplication.processEvents()
            time.sleep(0.1)
        #if statement needed, when server collected all players (OK TRUE)
        
        
    def init(self,path="resources/table.png"):
       
       #print(str(screenWidth))
       print(path)
       self.initScreenSize()
       self.initBackground(993,path)
       #gameInitial
       self.setPawnsOnStartingPosiotions()
       
    def setPawnsOnStartingPosiotions(self):
        rolesArray = self.getPlayersRoles()
        for i in rolesArray:
            if i == self.red:
                self.createPawns(self.redPawnsStartingPosition,'resources/redPawn.png',self.redPawns)
            if i == self.blue:
                self.createPawns(self.bluePawnsStartingPosition,'resources/bluePawn.png',self.bluePawns)
            if i == self.green:
                self.createPawns(self.greenPawnsStartingPosition,'resources/greenPawn.png',self.greenPawns)
            if i == self.yellow:
                self.createPawns(self.yellowPawnsStartingPosition,'resources/yellowPawn.png',self.yellowPawns)
    
        
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
    def createPawns(self,position,path,pawns):
        """
            wazne jest aby zapamietac obrazki pionkow bardzo wazne
        """
        j = 0
        for i in position:
            pawns.append(self.createImage(path))
            pawns[j].move(i[0],i[1])
            j+=1
        
    def createImage(self,path):
        label = QLabel(self)
        Image = QImage(path)
        
        label.setPixmap(QPixmap.fromImage(Image.scaled(75,75)))
        label.setScaledContents(False)
        
        label.setAlignment(Qt.AlignCenter)
        
    
        return label    
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
    
    

   

