from game.player import *
from .position import *
from .pawn import *
import random

class GameState:

    def __init__(self):
        super().__init__()
        self.dictOfPlayers = {k: createPlayer(k) for k in START_PLACES.keys()}
        self.__updatePawns()
        self.dice = 0
        self.turn = ""
        self.turnGenerator= self.__nextTurnGenerator()

    def __str__(self):

        self.getpawns()
        return str(self.dictOfPlayers[RED]) + \
               str(self.dictOfPlayers[GREEN]) + \
               str(self.dictOfPlayers[YELLOW]) + \
               str(self.dictOfPlayers[BLUE])

    def getpawns(self):
        return [x for i in [self.dictOfPlayers[RED], self.dictOfPlayers[GREEN], self.dictOfPlayers[YELLOW],
                            self.dictOfPlayers[BLUE]] for x in i.pawns]

    # TODO pola źle się dodają i typ się nie zmienia
    def tryToReplacePawn(self, position, steps,color):
        tpawn = self.__findPawn(Pawn(color,position.number,position.typeOfPosition,START_PLACES[color]))
        print("Typ position: ",type(position.number))
        print("Typ steps: ",type(steps))
        print("Kolor: ",color)
        newPosition = self.addStepsToPositon(position, steps,color)
        if self.__checkForWinPlace(tpawn, newPosition):
            tpawn.position = self.__generateEmptyPlace(tpawn.color, WIN_POSITION)
            return
        if self.__checkForFight(newPosition):
            epawn = self.__findPawnByPosition(newPosition)
            epawn.position = Position(epawn.idOfStartPlace,START_POSITION)
        if tpawn.position.typeOfPosition == START_POSITION:
            tpawn.position = Position(START_PLACES[tpawn.color], NORMAL_POSITION)
            return
        tpawn.position = newPosition

    def addStepsToPositon(self,position: Position, steps: int, color: str)-> Position:
        if(position.typeOfPosition == START_POSITION):
            return Position( START_PLACES[color], NORMAL_POSITION)
        return Position( (int(position.number) + int(steps) ) % (WIN_PLACES[RED] +1), position.typeOfPosition)

    def __findPawnByPosition(self, position):
        for pawn in self.pawns:
            if pawn.position == position:
                return pawn
        return None

    def __findPawn(self, searchedPawn):
        for pawn in self.pawns:
            if pawn == searchedPawn:
                return pawn
        return None

    def __checkForWinPlace(self, pawn: Pawn, newPosition: Position) -> bool:
        if pawn.position.typeOfPosition == NORMAL_POSITION:
            if (pawn.color == RED and  pawn.position.number > newPosition.number):
                return True
            elif newPosition.number >= WIN_PLACES[pawn.color] + 1 > pawn.position.number  and pawn.position.number < newPosition.number :
                return True
        return False

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
            w = 0
            for i in self.dictOfPlayers[k].pawns:
                if i.position.typeOfPosition == WIN_POSITION:
                    w +=1
                if w == 4:
                    return k
        return None


    def __nextTurnGenerator(self):
        while True:
            for i in self.dictOfPlayers.keys():
                yield i

    def nextTurn(self):
        return next(self.turnGenerator)

    def getDiceNumber(self):
        return random.choice(list(range(1,7)))

    def setDictOfPlayers(self, newDict):
        self.dictOfPlayers = newDict


    def __updatePawns(self):
        self.pawns = self.getpawns()
    #R[S1,W2,N3,S2]Y[]B[]G[]

def parseToGameState(text):
    tmpGameState = GameState()
    players = text.split("]")
    for player in players[:-1]:
        tmpPlayer = parseToPlayer(player)
        tmpGameState.setPlayer(tmpPlayer)
    return tmpGameState


