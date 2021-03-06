import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from client.ClientAPI import *
import random
import game.player
import game.position
import game.pawn
import time

class GamePanel(QWidget):
    port = 65432
    connected = True
    ipAdress = '127.0.0.1'
    role = 1  # colour of client

    red = 1
    blue = 2
    green = 3
    yellow = 4
    # Coordinates
    redPawnsStartingPositionsCoordinates = [[22, 26], [110, 24], [110, 104], [22, 108]]
    bluePawnsStartingPositionsCoordinates = [[788, 22], [880, 22], [880, 102], [790, 104]]
    greenPawnsStartingPositionsCoordinates = [[880, 798], [880, 892], [792, 890], [792, 800]]
    yellowPawnsStartingPositionsCoordinates = [[108, 888], [24, 890], [22, 794], [110, 794]]

    starterPositionsCoordinates = [[24, 370], [544, 22], [880, 544], [366, 882]]
    milieusPositionsCoordinates = [[24, 370], [98, 370], [182, 370], [264, 370], [366, 366], [366, 278],
                                   [366, 192], [366, 104], [366, 28], [456, 24], [544, 22], [544, 102],
                                   [544, 184], [544, 266], [544, 362], [622, 366], [708, 366], [796, 366],
                                   [880, 366], [880, 456], [880, 542], [798, 544], [710, 544], [622, 544],
                                   [544, 544], [544, 626], [544, 708], [544, 790], [544, 886], [458, 886],
                                   [368, 882], [368, 800], [368, 714], [368, 626], [368, 544], [266, 540],
                                   [182, 540], [100, 540], [26, 540], [26, 460]]

    winnerPositionsCoordinates = [[[106, 456], [194, 458], [282, 458], [364, 456]],
                                  [[452, 108], [452, 194], [452, 280], [452, 362]],
                                  [[798, 454], [716, 454], [628, 454], [542, 454]],
                                  [[454, 802], [454, 716], [454, 628], [454, 546]]]

    dicesPositionCoordinates = [[238, 235], [667, 233], [668, 672], [239, 669]]
    # lists of labels
    redPawnsStartingPosiotions = []
    bluePawnsStartingPosiotions = []
    greenPawnsStartingPosiotions = []
    yellowPawnsStartingPosiotions = []

    starterPositions = []
    # surroundings layer
    milieusPositions = []
    # winning Posistions
    redWinningPositions = []
    blueWinningPositions = []
    greenWinningPositions = []
    yellowWinningPositions = []
    # dice
    dicePositions = []
    # current posistions of pawns
    # list of label that pawn have
    redPawns = []
    bluePawns = []
    greenPawns = []
    yellowPawns = []

    ##place for more positions

    def __init__(self, parent, ipAdress='127.0.0.1', port=6669):
        super().__init__()
        self.serverGameAPI = API(self.ipAdress, self.connected);
        self.port = port
        self.ipAdress = ipAdress
        ##GIF WAITING staff

        self.initScreenSize()
        self.initBackground(993, 'resources/wait.jpg')

        self.show()
        self.waitForPlayers()
        self.init()
        self.gameStart()

    def waitForPlayers(self):

        for n in range(20):
            QApplication.processEvents()
            time.sleep(0.1)
        # if statement needed, when server collected all players (OK TRUE)

    # def moveOnScreen(self):

    def init(self, path="resources/table.png"):

        self.initScreenSize()
        self.initBackground(993, path)
        self.setAllPawnsPosiotions()
        self.skipButton()
        self.setPawnsImages()
        self.setDicesImages()

    def setAllPawnsPosiotions(self):
        self.createPawnPosiotions(self.redPawnsStartingPositionsCoordinates, self.redPawnsStartingPosiotions)
        self.createPawnPosiotions(self.bluePawnsStartingPositionsCoordinates, self.bluePawnsStartingPosiotions)
        self.createPawnPosiotions(self.greenPawnsStartingPositionsCoordinates, self.greenPawnsStartingPosiotions)
        self.createPawnPosiotions(self.yellowPawnsStartingPositionsCoordinates, self.yellowPawnsStartingPosiotions)
        self.createPawnPosiotions(self.starterPositionsCoordinates, self.starterPositions)
        self.createPawnPosiotions(self.milieusPositionsCoordinates, self.milieusPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[0], self.redWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[1], self.blueWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[2], self.greenWinningPositions)
        self.createPawnPosiotions(self.winnerPositionsCoordinates[3], self.yellowWinningPositions)
        self.createPawnPosiotions(self.dicesPositionCoordinates, self.dicePositions)
        ##TODO REST OF POSISTIONS

    def setPawnsImages(self):
        self.redPawnImage = self.createPawn('resources/redPawn.png')
        self.bluePawnImage = self.createPawn('resources/bluePawn.png')
        self.greenPawnImage = self.createPawn('resources/greenPawn.png')
        self.yellowPawnImage = self.createPawn('resources/yellowPawn.png')

    def setDicesImages(self):
        self.diceImage = []
        path = 'resources/k'
        for i in range(1, 7):
            Image = self.createDice('resources/k' + str(i) + '.png')
            self.diceImage.append(Image)

    def updateGameState(self):
        self.mergePawns(self.redPawns, self.serverGameAPI.PLAY.dictOfPlayers[game.player.RED])
        self.mergePawns(self.bluePawns, self.serverGameAPI.PLAY.dictOfPlayers[game.player.BLUE])
        self.mergePawns(self.greenPawns, self.serverGameAPI.PLAY.dictOfPlayers[game.player.GREEN])
        self.mergePawns(self.yellowPawns, self.serverGameAPI.PLAY.dictOfPlayers[game.player.YELLOW])
        if self.serverGameAPI.IS_WIN:
            print(self.serverGameAPI.WINNER)

    def mergePawns(self, pawnsOfClient, pawnsOfServer):
        for i in range(4):
            result = pawnsOfClient[i].position - self.convertPositions(pawnsOfServer[i].position,
                                                                       pawnsOfServer[i].color)
            pawnsOfClient[i].setPosition(result)
            self.movePawn(pawnsOfClient[i], pawnsOfClient[i].getPosition())

    def convertPositions(self, serverPosition, color):
        if serverPosition.typeOfPosition == game.position.START_POSITION:
            return -1
        if serverPosition.typeOfPosition == game.position.WIN_POSITION:
            return serverPosition.number + 39

        if color == 'Blue':
            result = (serverPosition.number - 10)
            if result < 0:
                result = 40 - result
        elif color == 'Green':
            result = (serverPosition.number - 20)
            if result < 0:
                result = 40 - result
        elif color == 'Yellow':
            result = (serverPosition.number - 30)
            if result < 0:
                result = 40 - result
        return result

    def gameStart(self):
        if self.serverGameAPI.RULE == game.player.RED:
            self.role = self.redPawns
        elif self.serverGameAPI.RULE == game.player.YELLOW:
            self.role = self.yellowPawns
        elif self.serverGameAPI.RULE == game.player.BLUE:
            self.role = self.bluePawns
        elif self.serverGameAPI.RULE == game.player.GREEN:
            self.role = self.greenPawns

        # asking server about players roles and quantity
        # this we need from server if red so redPawns we have
        self.role = self.yellowPawns
        self.setPawnsOnStartingPosiotions()

        self.setDiceOnStartPosition()
       # noOneWins = True
        flag = True
        while not self.serverGameAPI.IS_WIN:
            if self.serverGameAPI.IS_GAME_STARTED:
                if self.serverGameAPI.COLOR == game.player.RED and flag:
                    self.serverGameAPI.sendMove("S1");
                    flag = not flag
                print(self.serverGameAPI.PLAY)
            QApplication.processEvents()
            time.sleep(0.01)

    def pawnEvent(self):
        pawnToSend = None
        ww = None
        if self.serverGameAPI.PLAY.turn == self.role[0].getColor().upper()[0]:
            for i in self.role:
                if i.getCurrentPosition() == self.sender():

                    pos = i.position
                    if pos == -1 and self.dice.currentSide == 6:
                        pos = 0
                    else:
                        pos = i.position + self.dice.currentSide

                    isKanibal = False
                    for J in self.role:
                        if J.position == pos:
                            isKanibal = True
                            break
                    if not isKanibal:
                        i.setPosition(self.dice.currentSide)
                        ww = i.getPosition()
                        self.movePawn(i, ww)
                    pawnToSend = i
                    break
        if self.serverGameAPI.PLAY.turn == self.role[0].getColor().upper()[0]:
            if ww != 0:
                self.c
                self.serverGameAPI.sendMove()
                self.serverGameAPI.PLAY.turn = "DUPA"
        self.updateGameState()

    def convertToServerNotation(self, pawn):
        if pawn.position == -1:
            return game.pawn.Pawn(pawn.getColor()[0].upper(), pawn.ID, game.position.START_POSITION, 0)
        if pawn.position > 39:
            return game.pawn.Pawn(pawn.getColor()[0].upper(), pawn.position - 39, game.position.WIN_POSITION, 0)
        return game.pawn.Pawn(pawn.getColor()[0].upper(), (pawn.position + pawn.enterPosition) % 40,
                              game.position.NORMAL_POSITION, 0)

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                     quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

    def skipButton(self):
        self.skip = QPushButton(self)
        self.skip.setText('SKIP')
        self.skip.setGeometry(993 // 2 - 50, 993 // 2 - 50, 90, 90)
        # self.skip.setAlignment(Qt.AlignCenter)
        # self.skip.setScaledContents(False)
        self.skip.setStyleSheet(
            "QPushButton {color: BLACK;background-color:#FFFFFF;border-style: outset;border: 5px solid black;border-radius: 45px;font-size: 25px;font-family: Arial;font-weight: bold;}QPushButton:hover:!pressed{color: WHITE;background-color:#151515;border-style: outset;border: 5px solid white;border-radius: 45px;font-size: 25px;font-family: Arial;font-weight: bold;} ")
        self.skip.setVisible(True)
        self.skip.clicked.connect(self.skipEvent)
        print(self.skip)

    def skipEvent(self):
        # nextTurn
        self.setDiceOnPosition(self.dice, self.roleTheDice())
        print(self.sender().text())

    def movePawn(self, pawn, destinationPosition):
        if destinationPosition == 0:
            return
        pawn.getCurrentPosition().setVisible(False)
        pawn.setCurrentPosition(destinationPosition)
        self.setPawnOnPosition(pawn)

    def setDiceOnStartPosition(self):
        self.dice = Dice(self.dicePositions[0], self.diceImage)
        self.setDiceOnPosition(self.dice, self.roleTheDice())

    def setDiceOnPosition(self, dice, number):
        dice.getCurrentPosition().setPixmap(QPixmap.fromImage(dice.getSideByNumber(number)))
        dice.getCurrentPosition().setScaledContents(False)
        dice.getCurrentPosition().setVisible(True)
        dice.getCurrentPosition().setAlignment(Qt.AlignCenter)

    def roleTheDice(self):
        # zakres 1 - 6
        return random.randint(1, 6)

    def setPawnsOnStartingPosiotions(self):
        rolesArray = self.getPlayersRoles()
        for i in rolesArray:
            j = 0
            if i == self.red:
                for i in self.redPawnsStartingPosiotions:
                    # Pawn creations
                    self.redPawns.append(
                        Pawn(i, self.redPawnImage, 'red', 0, self.redWinningPositions, self.milieusPositions,
                             self.redPawnsStartingPositionsCoordinates[j], j))
                    self.setPawnOnPosition(self.redPawns[j])
                    j += 1
            elif i == self.blue:
                for i in self.bluePawnsStartingPosiotions:
                    self.bluePawns.append(
                        Pawn(i, self.bluePawnImage, 'blue', 10, self.blueWinningPositions, self.milieusPositions,
                             self.bluePawnsStartingPositionsCoordinates[j], j))
                    self.setPawnOnPosition(self.bluePawns[j])
                    j += 1
            elif i == self.green:
                for i in self.greenPawnsStartingPosiotions:
                    self.greenPawns.append(
                        Pawn(i, self.greenPawnImage, 'green', 20, self.greenWinningPositions, self.milieusPositions,
                             self.greenPawnsStartingPositionsCoordinates[j], j))
                    self.setPawnOnPosition(self.greenPawns[j])
                    j += 1
            elif i == self.yellow:
                for i in self.yellowPawnsStartingPosiotions:
                    self.yellowPawns.append(
                        Pawn(i, self.yellowPawnImage, 'yellow', 30, self.yellowWinningPositions, self.milieusPositions,
                             self.yellowPawnsStartingPositionsCoordinates[j], j))
                    self.setPawnOnPosition(self.yellowPawns[j])
                    j += 1

    def createPawnPosiotions(self, coordinates, posiotions):

        j = 0
        for i in coordinates:
            posiotions.append(ClickLabel(self))
            posiotions[j].move(i[0], i[1])

            j += 1

    def setPawnOnPosition(self, pawn):
        pawn.getCurrentPosition().setPixmap(QPixmap.fromImage(pawn.getColor()))
        pawn.getCurrentPosition().setScaledContents(False)
        pawn.getCurrentPosition().setVisible(True)
        pawn.getCurrentPosition().setAlignment(Qt.AlignCenter)
        pawn.getCurrentPosition().setStyleSheet(
            'QLabel{border: 1px solid white;border-style: outset;border-radius: 37px;}QLabel:hover{border: 17px solid ' + pawn.getColorName() + ';border-radius: 37px;}')
        pawn.getCurrentPosition().clicked.connect(self.pawnEvent)

    def createDice(self, path):
        Image = QImage(path)
        Image = Image.scaled(100, 100)
        return Image

    def createPawn(self, path):
        Image = QImage(path)
        Image = Image.scaled(75, 75)
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
        tempArray = [1, 2, 3, 4]
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

    # Screen Settings
    def initScreenSize(self):

        self.move(993 // 2, 0)
        self.resize(993, 993)
        self.setFixedSize(self.size())
        return 993

    def initBackground(self, screenWidth, path):
        oImage = QImage(path)
        sImage = oImage.scaled(QSize(screenWidth, screenWidth))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)


class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class Pawn():
    def __init__(self, posistion, color, colorName,
                 enterPosition, WinningPositions,
                 NormalPositions, cordinates, id):

        # TODO Dupad
        self.ID = id
        self.startPositioncoordinates = cordinates
        # Qlabel
        self.startPosition = posistion
        self.currentPosition = posistion
        # String and Image
        self.pawnColor = color
        self.colorName = colorName
        # position in number
        self.position = -1
        # enterPosition as number int
        self.enterPosition = enterPosition
        self.WinningPositions = WinningPositions
        self.NormalPositions = NormalPositions
        self.changeBool = False

    def getCurrentPosition(self):
        return self.currentPosition

    def getColor(self):
        return self.pawnColor

    def setCurrentPosition(self, position):
        self.currentPosition = position

    def getColorName(self):
        return self.colorName

    def setPosition(self, add):
        ##bardzo wczesna wersja 149

        if add < 0:
            self.position = -1
            self.changeBool = True
        elif self.position == -1 and add == 6:
            self.position = 0
            self.changeBool = True

        elif self.position > -1 and 43 >= (self.position + add):
            self.position += add

            self.changeBool = True
        else:
            self.changeBool = False
        print('setPosition: ' + str(self.changeBool))
        # TODO zrobic tutaj piekna walidacje dodac z kartki rzeczy czyli translacja na 0 - 39 ale kazdy obiekt widzi jakby to on mial od 0 do 39 position a bedzie innaczej wyswietlany (z przesunieciem tylko)

    def getPosition(self):
        if not self.changeBool:
            print('getPosition: ' + str(self.changeBool))
            return 0
        elif self.position == -1:
            return self.startPosition
        elif self.position >= 0 and self.position <= 39:
            print('getPosition: ' + str(self.changeBool))
            return self.NormalPositions[(self.position + self.enterPosition) % 40]
        elif self.position >= 40 and self.position <= 43:
            print('getPosition: ' + str(self.changeBool))
            return self.WinningPositions[self.position - 40]

        return 0


class Dice():
    def __init__(self, posistion, sidesImages):
        self.currentPosition = posistion
        self.sidesImages = sidesImages
        self.currentSide = 1

    def getSideByNumber(self, number):
        self.currentSide = number
        print(number)
        return self.sidesImages[number - 1]

    def setCurrentPosition(self, position):
        self.currentPosition = position

    def getCurrentPosition(self):
        return self.currentPosition

    def getCurrentSide(self):
        return self.currentSide


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    # app.setStyleSheet('QWidget{background-color:black}')
    oMainwindow = GamePanel(app)
    sys.exit(app.exec_())
