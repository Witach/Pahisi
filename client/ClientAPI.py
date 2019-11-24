import socket
import game.gameState
MOVE_MESSAGE = "MOVE;{position}"
SEPARATOR = ";"
HOST = '127.0.0.1'
PORT = 65432
COLOR = ""
PLAY = ""

INFO = "INFO"
WIN = "WIN"
RULE = "RULE"
WINNER = ""
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def __parserToFunction(task):
    if task[0] == INFO:
        def fun():
            __infoFunction(task[1], task[2], task[3])
            return False

        return fun
    if task[0] == WIN:
        def fun():
            __winFun(task[1])
            return True

        return fun
    return None

def __winFun(turn):
    global WINNER
    WINNER = turn


def __infoFunction(turn, dice, gamestate):
    global PLAY
    tmpPlay = game.gameState.parseToGameState(gamestate)
    PLAY.setDictOfPlayers(tmpPlay.dictOfPlayers)
    PLAY.turn = turn
    PLAY.dice = dice

def __ruleFunction(turn):
    global COLOR
    COLOR = turn

def updateGame():
    global SOCK
    data = SOCK.recv(1024)
    fun = __parserToFunction(data)
    return fun()

def sendMove(position):
    global SOCK
    SOCK.sendAll(MOVE_MESSAGE.format(position=position))

SOCK.connect((HOST, PORT))
data = SOCK.recv(1024)
data = data.decode(encoding="UTF-8")
tokens = data.split(SEPARATOR)
print(tokens)
__ruleFunction(tokens[1])
PLAY = game.gameState.GameState()

