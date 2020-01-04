from game import pawn
from game.pawn import parseToPawn
from game.position import *

RED = "R"
BLUE = "B"
YELLOW = "Y"
GREEN = "G"

ID_OF_RED = 0
ID_OF_BLUE = 10
ID_OF_GREEN = 20
ID_OF_YELLOW = 30

START_PLACES = {RED: ID_OF_RED,
                BLUE: ID_OF_BLUE,
                GREEN: ID_OF_GREEN,
                YELLOW: ID_OF_YELLOW
                }

WIN_PLACES = {RED: 39,
              BLUE: ID_OF_BLUE - 1,
              GREEN: ID_OF_GREEN - 1,
              YELLOW: ID_OF_YELLOW - 1
              }


class Player:
    color = ""
    pawns = []

    def __init__(self, color, pawns):
        super().__init__()
        self.color = color
        self.pawns = pawns

    def __str__(self):
        res = self.color[0]
        res += "["
        for index , pawn in  enumerate(self.pawns):
            res += str(pawn)
            if index != 3:
                res += ","
        res += "]"
        return res

    def getEmptyPlace(self, typeOfPosition):
        list_of_Places = [i.position.number for i in self.pawns if i.position.typeOfPosition == typeOfPosition]
        for i in range(4):
            try:
                list_of_Places.index(i)
            except ValueError:
                return i
        return 0


def createPlayer(color):
    return Player(color, [
        pawn.Pawn(color, 0, START_POSITION,0),
        pawn.Pawn(color, 1, START_POSITION,1),
        pawn.Pawn(color, 2, START_POSITION,2),
        pawn.Pawn(color, 3, START_POSITION,3),
    ])

def parseToPlayer(text):
    print("="*20)
    print(text)
    playerTokens = text.split("[")
    print("playerTokens[1].split(",")")
    print(playerTokens[1].split(","))
    print("playerTokens[1].split(", ")")
    pawnsTokens =  playerTokens[1].split(",")
    pawns = []
    for pawn in pawnsTokens:
        tmpPawn = parseToPawn(pawn)
        tmpPawn.color = playerTokens[0]
        pawns.append(tmpPawn)
    nativePlayer = Player(playerTokens[0],pawns)
    return nativePlayer