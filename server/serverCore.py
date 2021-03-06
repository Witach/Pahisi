import socket
from game.gameState import *

INFO_MESSAGE = "INFO;{turn};{dice};{gamestate}%"
RULE_MESSAGE = "RULE;{turn}%"
WIN_MESSAGE = "WIN;{turn}%"
START_MESSAGE = "START%"
HOST = '127.0.0.1'
PORT = 65432
ENCODING = "UTF-8"
#R[S1,S2,S3]$
TEST = True

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST,PORT))
        gameLogic(sock)


def gameLogic(sock):
    print("try to preppare players")
    dictOfSockets = preparePlayers(sock)
    print("players are prepared")
    play = GameState()

    if TEST :
        testInit(play)

    print("game is made")
    bytesOfMessage = bytes(START_MESSAGE, ENCODING)
    print(bytesOfMessage)
    for i in [RED,GREEN,BLUE,YELLOW]:
        dictOfSockets[i].send(bytesOfMessage)
    while play.checkForWinner() is None:
        print("Nest turn")
        COLOR = str(play.nextTurn())
        print("color is chosen")
        DICE = play.getDiceNumber()
        print("dice is chosen")
        bytesOfMessage = bytes(INFO_MESSAGE.format(turn=COLOR, dice=DICE, gamestate=str(play)),ENCODING)
        print(bytesOfMessage)
        for i in [RED, GREEN, BLUE, YELLOW]:
            dictOfSockets[i].send(bytesOfMessage)
        print("Game state was sended to all players")
        CONN = dictOfSockets[COLOR]
        print("next player is being asked for move")
        DATA = CONN.recv(1024)
        DATA = str(DATA)[2:-1]
        if DATA == "SKIP":
            print("PLayer Have Skipped")
            continue
        MOVE = parseToMove(DATA)
        print("try to move pawn")
        play.tryToReplacePawn(MOVE,DICE,COLOR)
    bytesOfMessage = bytes(INFO_MESSAGE.format(turn=COLOR, dice=DICE, gamestate=str(play)), ENCODING)
    print(bytesOfMessage)
    for i in [RED, GREEN, BLUE, YELLOW]:
        dictOfSockets[i].send(bytesOfMessage)
    print("server sends info about who is the winner")
    bytesOfMessage = bytes(WIN_MESSAGE.format(turn=play.checkForWinner()[0]),encoding=ENCODING)
    for i in [RED, GREEN, BLUE, YELLOW]:
        dictOfSockets[i].send(bytesOfMessage)
        dictOfSockets[i].close()

def testInit(play):
    if TEST:
        play.dictOfPlayers[RED].pawns[0].position.number = 0
        play.dictOfPlayers[RED].pawns[0].position.typeOfPosition = WIN_POSITION
        play.dictOfPlayers[RED].pawns[1].position.number = 1
        play.dictOfPlayers[RED].pawns[1].position.typeOfPosition = WIN_POSITION
        play.dictOfPlayers[RED].pawns[2].position.number = 2
        play.dictOfPlayers[RED].pawns[2].position.typeOfPosition = WIN_POSITION
        play.dictOfPlayers[RED].pawns[3].position.number = 39
        play.dictOfPlayers[RED].pawns[3].position.typeOfPosition = NORMAL_POSITION

def preparePlayers(sock):
    dictOfSockets = {}
    for i in [RED, YELLOW, BLUE, GREEN]:
        sock.listen()
        conn, addr = sock.accept()
        bytesOfMessage = bytes(RULE_MESSAGE.format(turn=i[0]),ENCODING)
        conn.send(bytesOfMessage)
        dictOfSockets[i] = conn
    return dictOfSockets


def parseToMove(message):
    tokens = message.split(";")
    typeOfPistion = tokens[1][0]
    print("Move: ",tokens)
    number = tokens[1][1:]
    return Position(number,typeOfPistion)
