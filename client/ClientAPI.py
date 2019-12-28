import socket
import game.gameState
import threading

class API():

    MOVE_MESSAGE = "MOVE;{position}"
    SEPARATOR = ";"
    IS_GAME_STARTED = False;
    HOST = '127.0.0.1'
    PORT = 65432
    COLOR = ""
    PLAY = game.gameState.GameState()
    IS_WIN = False

    INFO = "INFO"
    WIN = "WIN"
    START = "START";
    RULE = "RULE"
    WINNER = ""
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,IP,PORT2):
        self.PORT = PORT2
        self.HOST = IP
        print(str(self.PORT))
        print(str(self.HOST))
        self.SOCK.connect((self.HOST, 65432))
        data = self.SOCK.recv(1024)
        data = data.decode(encoding="UTF-8")
        tokens = data.split("%")[0].split(self.SEPARATOR)
        print(tokens)
        self.__ruleFunction(tokens[1])
        self.PLAY = game.gameState.GameState()
        self.__startListener()

    def __parserToFunction(self,task):
        if task[0] == self.INFO:

            def fun():
                self.__infoFunction(task[1], task[2], task[3])
                return False

            return fun

        if task[0] == self.WIN:

            def fun():
                self.__winFun(task[1])
                return True

            return fun

        if task[0] == self.START:

            def fun():
                self.__startfun()
                return False

            return fun

        return None

    def __winFun(self,turn):
        self.WINNER = turn


    def __infoFunction(self,turn, dice, gamestate):
        tmpPlay = game.gameState.parseToGameState(gamestate)
        self.PLAY.setDictOfPlayers(tmpPlay.dictOfPlayers)
        self.PLAY.turn = turn
        self.PLAY.dice = dice
        print("Dice" + str(dice))

    def __ruleFunction(self,turn):
        self.COLOR = turn

    # z servera może przyjść kilka tasków na raz !!!
    def updateGame(self):
        while True:
            data = self.SOCK.recv(1024)
            dataStr = str(data)[2:-1]
            for index, task in enumerate(dataStr.split("%")):
                if index != len(dataStr.split("%")) - 1:
                    fun = self.__parserToFunction(task.split(self.SEPARATOR))
                    self.IS_WIN = fun()

    def sendMove(self,position):
        bytesOfMessage = bytes(self.MOVE_MESSAGE.format(position=position),"UTF-8")
        self.SOCK.send(bytesOfMessage)

    def __startfun(self):
        self.IS_GAME_STARTED = True;

    def __startListener(self):
        x = threading.Thread(target=self.updateGame)
        x.start()