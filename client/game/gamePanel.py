import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from win32api import GetSystemMetrics
import time
import threading
class GamePanel(QWidget):
    port = 6669
    connected = True
    ipAdress = '127.0.0.1'
    
    def __init__(self,app,ipAdress = '127.0.0.1',port = 6669):
       super().__init__()
       app.setStyleSheet('QWidget{background-color:black;}')
       self.port = port
       self.ipAdress = ipAdress
       ##GIF WAITING staff
       self.initGifWaiting()
       ##WAITING FOR CONNECTION THREAD
       x = threading.Thread(target=self.waitingForConnection, args=())
       x.start()
       
       self.show()
    def initGifWaiting(self):
        self.initScreenSize()
        self.movie =  self.createLabelGif('resources/waiting.gif',75)
        self.oLayout = QVBoxLayout()
        self.oLayout.addWidget(self.movie)
        self.setLayout(self.oLayout)
    def init(self):
       screenWidth = self.initScreenSize()
       self.initBackground(screenWidth)
    #Screen Settings   
    def initScreenSize(self):
       screenWidth = (int)(GetSystemMetrics(1) -  0.08*GetSystemMetrics(1))
       self.move((int)(GetSystemMetrics(1)/2),0)
       self.resize(screenWidth,screenWidth)
       self.setFixedSize(self.size())
       return screenWidth
   
    def initBackground(self,screenWidth):
       oImage = QImage('resources/table.png')
       sImage = oImage.scaled(QSize(screenWidth,screenWidth))                   # resize Image to widgets size
       palette = QPalette()
       palette.setBrush(QPalette.Background, QBrush(sImage))                        
       self.setPalette(palette)
       
    ## GIF STAFF   
    def createLabelGif(self,filename,speed):
        movie = self.loadFileIntoMovie(filename)
        movieScreen = self.makeLabelfitTheGif()
        self.addTheMovieOBjectToTheLabel(movie,speed,movieScreen)
        return movieScreen
        
    def loadFileIntoMovie(self,filename):
        movie = QMovie(filename, QByteArray(), self)
        movie.setScaledSize(QSize().scaled(GetSystemMetrics(1) -  0.08*GetSystemMetrics(1),GetSystemMetrics(1) -  0.08*GetSystemMetrics(1),Qt.KeepAspectRatio))
        return movie
        
    def makeLabelfitTheGif(self):
        movie_screen = QLabel()
        movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        movie_screen.setAlignment(Qt.AlignCenter)
        return movie_screen   
    
    def addTheMovieOBjectToTheLabel(self, movie,speed,movie_screen):
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(speed)
        movie_screen.setMovie(movie)
        movie.start()  
     ## GIF STAFF 
     ## Waiting for connection
    def waitingForConnection(self):
        #wait for connection in loop
        #need connection checked
        
        time.sleep(2)
        
        if self.connected:
            #if connected then delete waiting gif
            self.oLayout.itemAt(0).widget().setParent(None)
            self.init()
             
   

          
    

      

       

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('QWidget{background-color:black}')
    oMainwindow = GamePanel(app)
    sys.exit(app.exec_())
    
    

   

