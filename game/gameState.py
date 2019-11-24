from game.player import *
from .position import *
from game.pawn import *
import random

class GameState:

    def __init__(self):
        super().__init__()
        self.dictOfPlayers = {k: createPlayer(k) for k in START_PLACES.keys()}
        self.__updatePawns()
        self.dice = 0
        self.turn = ""

    def __str__(self):
        return str(self.dictOfPlayers[RED]) + \
               str(self.dictOfPlayers[GREEN]) + \
               str(self.dictOfPlayers[YELLOW]) + \
               str(self.dictOfPlayers[BLUE])

    def __getpawns(self):
        return [x for i in [self.dictOfPlayers[RED], self.dictOfPlayers[GREEN], self.dictOfPlayers[YELLOW],
                            self.dictOfPlayers[BLUE]] for x in i.pawns]

    def tryToReplacePawn(self, position, steps):
        tpawn = self.__findPawnByPosition(position)
        newPosition = Position(position.number + steps, position.typeOfPosition)
        if self.__checkForWinPlace(tpawn, newPosition):
            tpawn.position = self.__generateEmptyPlace(tpawn, WIN_POSITION)
            return
        if tpawn.position == START_POSITION:
            tpawn.position = Position(START_PLACES[tpawn.color], NORMAL_POSITION)
        if self.__checkForFight(newPosition):
            epawn = self.__findPawnByPosition(newPosition)
            epawn.position = self.__generateEmptyPlace(epawn, START_POSITION)
        tpawn.position = newPosition

    def __findPawnByPosition(self, position):
        for pawn in self.pawns:
            if pawn.position == position:
                return pawn
        return None

    def __checkForWinPlace(self, pawn, newPosition):
        return (pawn.position.number + newPosition.number) > self.WIN_PLACES[pawn.color]

    def __checkForFight(self, newPosition):
        return not self.__findPawnByPosition(newPosition) is None

    def __returnPawnToStart(self, pawn):
        pawn.position = START_POSITION

    def __generateEmptyPlace(self, color, typeOfPosition):
        return Position(self.dictOfPlayers[color].getEmptyPlace(typeOfPosition), typeOfPosition)

    def setPlayer(self,player):
        self.dictOfPlayers[player.color] = player
        self.__updatePawns()

    def checkForWinner(self):
        for k in self.dictOfPlayers.keys():
            for i in self.dictOfPlayers[k].pawns:
                if i.position.typeOfPosition == WIN_POSITION:
                    return k
        return None

    def nextTurn(self):
        while True:
            for i in self.dictOfPlayers.keys():
                yield i

    def getDiceNumber(self):
        return random.choice(list(range(1,7)))

    def setDictOfPlayers(self, newDict):
        self.dictOfPlayers = newDict


    def __updatePawns(self):
        self.pawns = self.__getpawns()
    #R[S1,W2,N3,S2]Y[]B[]G[]

def parseToGameState(text):
    tmpGameState = GameState()
    players = text.split("]")
    for player in players:
        tmpPlayer = parseToPlayer(player)
        tmpGameState.setPlayer(tmpPlayer)
    return tmpGameState


