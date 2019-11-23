import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from win32api import GetSystemMetrics
class GamePanel(QWidget):
    port = 6669
    ipAdress = '127.0.0.1'
    
    def __init__(self,ipAdress = '127.0.0.1',port = 6669):
       super().__init__()
       self.port = port
       self.ipAdress = ipAdress
       self.init()
       self.show()
    def init(self):
        
       screenWidth = self.initScreenSize()
       self.initBackground(screenWidth)
       
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
   
        

      

       

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color:orange;border: 1px solid black;}')
    oMainwindow = GamePanel()
    sys.exit(app.exec_())