import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from client.ClientAPI import *
import re
from enum import Enum
import game.player
import game.position
import game.pawn
import time
class PositionType(Enum):
    START = "S"
    NORMAL = "N"
    WINNING = "W"


class newGamePanel(QWidget):
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
    connected = True
    myTurn = False


    pawnsArray = []

    def __init__(self, parent, ipAdress='127.0.0.1'):
        super().__init__()
        self.serverGameAPI = API(ipAdress, True);
        self.__initScreenSize__()
        self.__printBackground__()
        self.__InitPawns__()
        self.__InitDice__()
        self.startGame()
    def __InitDice__(self):
        self.label = QLabel(self)
        self.setDice(1) #magia ?
        self.setDiceToPlayer("R") #dziala
    def __InitPawns__(self):
        for i in range(16):
            button = QPushButton(self)
            button.clicked.connect(self.pawnEvent)
            button.resize(75, 75)
            if i < 4:
                color = "red"
            elif i < 8:
                color = "green"
            elif i < 12:
                color = "yellow"
            else:
                color = "blue"
            button.setStyleSheet(
                "QPushButton "
                "{color: white;"
                "background-color:" + color + ";"
                                              "border-style: outset;"
                                              "border: 5px solid white;"
                                              "border-radius: 36px;font-size:"
                                              " 25px;font-family:"
                                              " Arial;font-weight:"
                                              " bold;"

                                              "}QPushButton:hover:!pressed"
                                              "{color: " + color + ";"
                                                                   "background-color:white;"
                                                                   "border-style: outset;border: 5px solid " + color + ";"
                                                                                                                       "border-radius: 36px;font-size: 25px;font-family: Arial;"
                                                                                                            "font-weight: bold;} ")

            self.pawnsArray.append( Pawn("S" + str(i % 4), button, color))

            # button.move(100, 70)
        self.myRoleSign = QPushButton(self);
        self.myRoleSign.resize(90, 90)
        self.myRoleSign.move(993 // 2 - 50,993 // 2 - 50)
        self.myRoleSign.clicked.connect(self.skipEvent)
        self.myRoleSign.setText("SKIP")
        self.winner = QLabel(self)
        self.winner.setVisible(False)
    def wait(self, sec=1):
        for n in range(sec * 10):
            QApplication.processEvents()
            time.sleep(0.1)
            # if statement needed, when server collected all players (OK TRUE)

        # def moveOnScreen(self):

    def startGame(self):

        if self.serverGameAPI.COLOR == "R":
            self.myPawns = self.pawnsArray[0:4]
        elif self.serverGameAPI.COLOR == "Y":
            self.myPawns = self.pawnsArray[8:12]
        elif self.serverGameAPI.COLOR == "B":
            self.myPawns = self.pawnsArray[12:16]
        elif self.serverGameAPI.COLOR == "G":
            self.myPawns = self.pawnsArray[4:8]

        self.myRoleSign.setStyleSheet("QPushButton {background-color: "+ self.myPawns[0].color + "; border-style: outset; border: 5px solid black; border-radius: 45px; font-size: 25px} QPushButton:hover:!pressed{ color: "+self.myPawns[0].color+" ;background-color:black;  border-style: outset; border: 5px solid " +self.myPawns[0].color+"; border-radius: 45px; font-size: 25px; }" )
        self.show()
        for i in self.myPawns:
            print(i.position + " " + i.color)
        self.__updateView__()
            # asking server about players roles and quantity
            # this we need from server if red so redPawns we have
        flaga = True
        while not self.serverGameAPI.IS_WIN:
            if self.serverGameAPI.IS_GAME_STARTED:
                if self.serverGameAPI.COLOR == self.serverGameAPI.PLAY.turn:
                    if flaga:
                        print("Twoja KOLEJ")
                    flaga = False
                    self.myTurn = True
                else:
                    flaga = True
                    self.myTurn = False
                self.__updatePawnsPositions__()
                self.setDiceToPlayer(self.serverGameAPI.PLAY.turn)
                self.setDice(self.serverGameAPI.PLAY.dice)
            QApplication.processEvents()
            time.sleep(0.0001)
        flagaa = True
        while True:


            self.winner.resize(993-20,100)
            self.winner.move(10,450)
            newfont = QFont("Times", 45, QFont.Bold)

            if self.serverGameAPI.WINNER == "R" and flagaa:
                self.winner.setStyleSheet("background-color: red")
                self.winner.setText(" WYGRAł GRACZ CZERWONY !!!")
            if self.serverGameAPI.WINNER == "B"  and flagaa:
                self.winner.setStyleSheet("background-color: blue")
                self.winner.setText(" WYGRAł GRACZ NIEBIESKI !!!")
            if self.serverGameAPI.WINNER == "G" and flagaa:
                self.winner.setStyleSheet("background-color: green")
                self.winner.setText(" WYGRAł GRACZ ZIELONY !!!")
            if self.serverGameAPI.WINNER == "Y" and flagaa:
                self.winner.setStyleSheet("background-color: yellow")
                self.winner.setText(" WYGRAł GRACZ ŻÓłTY !!!")
            self.winner.setFont(newfont)
            self.winner.setVisible(True)
            flagaa = False
            QApplication.processEvents()
            time.sleep(0.0001)


    # tutaj beda poruszane wszystkie pionki na swoje pozycje ktore otrzymaja od serwera ;)
    def __updatePawnsPositions__(self):
        #pozycje lista
        pawns = self.serverGameAPI.PLAY.getpawns()
        for i in range(len(pawns)): # zwrocil nam pawny
            pawn = self.pawnsArray[i]
            if not pawn.position == str(pawns[i].position.typeOfPosition) + str(pawns[i].position.number):
                print(self.serverGameAPI.PLAY)
                print("update "+pawn.position + " " + pawn.color + " vs " + str(pawns[i].position.typeOfPosition) + str(pawns[i].position.number) + " " + pawns[i].color)
            pawn.position = str(pawns[i].position.typeOfPosition) + str(pawns[i].position.number)
            self.pawnsArray[i] = pawn
        #tutaj chcemy zaaktualizowac pozycje wszystkich pionkow po czym wywoluje sie kolejna funkcja ktora ustawia te pionki na obrazie
        self.__updateView__()
    def pawnEvent(self):
        if self.myTurn and self.serverGameAPI.IS_GAME_STARTED:
            for i in self.myPawns:
                if i.QPushButtonID == self.sender():
                    canIgo = self.__caIgo(i.color, i.position, self.serverGameAPI.PLAY.dice)
                    print("can i go ? = " + str(canIgo))
                    if canIgo:
                        ifCannibal = self.ifCanibal(i, self.myPawns, self.serverGameAPI.PLAY.dice)
                        if not ifCannibal:
                            canIgo = False
                    print("can i go ? = " + str(canIgo))
                    print("Wybrany pionek => " + i.position)
                    print("Moj kolor => " + self.serverGameAPI.COLOR)

                    if canIgo:
                        self.serverGameAPI.sendMove(i.position)
                        print(self.serverGameAPI.PLAY)
                    else:
                        print("nie mozesz sie ruszyc tym pionkiem !")

    def skipEvent(self):
        if self.myTurn and self.serverGameAPI.IS_GAME_STARTED:
            print("SKIP")
            self.serverGameAPI.skipMove()
    def __caIgo(self, pawnColor, pawnPosition, dice):
        canIgo = False
        splittedPositioni = re.split('(\d+)', pawnPosition)
        number = splittedPositioni[1]
        type = splittedPositioni[0]
        print("type = " + type + " number = " + number + " dice = " + str(dice))
        if type == "N":
            canIgo = True
        elif (type == "S") and (dice == "6"):
            canIgo = True
        elif type == "W":
            canIgo = False
        return canIgo

    def ifCanibal(self, currentPawn, myPawns, dice):
        canIgo = True
        splittedPositioni = re.split('(\d+)', currentPawn.position)
        number = splittedPositioni[1]
        type = splittedPositioni[0]
        for i in myPawns:
            if currentPawn == i:
                continue
            splittedPositionj = re.split('(\d+)', i.position)
            numberi = splittedPositionj[1]
            typei = splittedPositionj[0]
            if currentPawn.color == "red":
                if type == "S" and typei == "N" and numberi == "0":
                    canIgo = False
                    break
                if type == "N":
                    numbernew, nowytyp  = self.__PawnColorTranslationNormal("red", int(number), int(dice))
                    print(str(nowytyp) + " == " + str(typei) + " and " + str(numbernew) + " == " + str(numberi))
                    if nowytyp == typei and numbernew == int(numberi):
                        canIgo = False
                        break
                if type == "W" and typei == "W" and int(numberi) == int((number) + int(dice)):
                    canIgo = False
                    break
            if currentPawn.color == "blue":
                if type == "S" and typei == "N" and numberi == "10":
                    canIgo = False
                    break
                if  type== "N":
                    nowytyp, numbernew = self.__PawnColorTranslationNormal("blue", int(number), int(dice))
                    if nowytyp == typei and numbernew == int(numberi):
                        canIgo = False
                        break
                if type == "W" and typei == "W" and int(numberi) == int(int(number) + int(dice)):
                    canIgo = False
                    break
            if currentPawn.color == "green":
                if type == "S" and typei == "N" and numberi == "20":
                    canIgo = False
                    break
                if type == "N":
                    nowytyp, numbernew = self.__PawnColorTranslationNormal("green", int(number), int(dice))
                    if nowytyp == typei and numbernew == int(numberi):
                        canIgo = False
                        break
                if type == "W" and typei == "W" and int(numberi) == int(int(number) + int(dice)):
                    canIgo = False
                    break
            if currentPawn.color == "yellow":
                if type == "S" and typei == "N" and numberi == "30":
                    canIgo = False
                    break
                if type == "N":
                    nowytyp, numbernew = self.__PawnColorTranslationNormal("yellow", int(number), int(dice))
                    if nowytyp == typei and numbernew == int(numberi):
                        canIgo = False
                        break
                if type == "W" and typei == "W" and int(numberi) == int(int(number) + int(dice)):
                    canIgo = False
                    break
        return canIgo

    def __PawnColorTranslationNormal(self,color,number,dice):


        if color == "red":
            if int(number) + int(dice) > 39:
                return (int(number) + int(dice))%40 + 10,"W"
            else:
                return (int(number)+  int(dice)),"N"
        if color == "blue":
            if int(number) < 10 and int(number) + int(dice) > 9:
                return (int(number) + int(dice))%10 + 10,"W"
            else:
                return (int(number) + int(dice)),"N"
        if color == "green":
            if int(number) < 20 and int(number) + int(dice) > 19:
                return (int(number) + int(dice))%20 + 10,"W"
            else:
                return (int(number) + int(dice)),"N"
        if color == "yellow":
            if int(number) < 30 and int(number) + int(dice) > 29:
                return (int(number) + int(dice))%30 + 10,"W"
            else:
                return (int(number) + int(dice)),"N"
    def __updateView__(self):
        for pawn in self.pawnsArray:

            splittedPosition = re.split('(\d+)',pawn.position)
            coordinates = self.__getPawnCoordinates__(splittedPosition[0],splittedPosition[1],pawn.color[0].upper())
            pawn.QPushButtonID.move(coordinates[0],coordinates[1])

    #parsuje tak naparwde kolory i inne na koordynaty dla przyciskow
    def __getPawnCoordinates__(self,type,numberString,color):
        number = int (numberString)
        if PositionType(type) == PositionType.START:
            if color == "R":
                return self.redPawnsStartingPositionsCoordinates[number]
            elif color == "B":
                return self.bluePawnsStartingPositionsCoordinates[number]
            elif color == "G":
                return self.greenPawnsStartingPositionsCoordinates[number]
            elif color == "Y":
                return self.yellowPawnsStartingPositionsCoordinates[number]
        elif PositionType(type) == PositionType.NORMAL:
            return self.milieusPositionsCoordinates[number]
        elif PositionType(type) == PositionType.WINNING:
            if color == "R":
                return self.winnerPositionsCoordinates[0][number]
            elif color == "B":
                return self.winnerPositionsCoordinates[1][number]
            elif color == "G":
                return self.winnerPositionsCoordinates[2][number]
            elif color == "Y":
                return self.winnerPositionsCoordinates[3][number]


    def __printBackground__(self, path="resources/table.png", screenWidth=993):
        oImage = QImage(path)
        sImage = oImage.scaled(QSize(screenWidth, screenWidth))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def __initScreenSize__(self):
        self.move(993 // 2, 0)
        self.resize(993, 993)
        self.setFixedSize(self.size())
        return 993
    def setDiceToPlayer(self,player):
        self.label.setVisible(True)

        if player == "R":
            self.label.move(self.dicesPositionCoordinates[0][0],self.dicesPositionCoordinates[0][1])
        elif player == "B":
            self.label.move(self.dicesPositionCoordinates[1][0], self.dicesPositionCoordinates[1][1])
        elif player == "G":
            self.label.move(self.dicesPositionCoordinates[2][0], self.dicesPositionCoordinates[2][1])
        elif player == "Y":
            self.label.move(self.dicesPositionCoordinates[3][0], self.dicesPositionCoordinates[3][1])
    def setDice(self,number):

        pixmap = QPixmap("resources/k" + str(number) + ".png")
        pixmap2 = pixmap.scaled(100,100)
        self.label.setPixmap(pixmap2)


class Pawn:
    def __init__(self, position, QPushButtonID,color):
        self.position = position
        self.startingPosition = position
        self.QPushButtonID = QPushButtonID
        self.color = color


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    # app.setStyleSheet('QWidget{background-color:black}')
    oMainwindow = newGamePanel(app)
    sys.exit(app.exec_())
