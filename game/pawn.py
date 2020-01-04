from .position import Position


class Pawn:

    position = ""
    color = ""
    idOfStartPlace = 0
    passedThroughStart = False

    def __init__(self, color,position, typeOfPisition,startPlace):
        self.color = color
        self.position = Position(position,typeOfPisition)
        self.idOfStartPlace = startPlace

    def __str__(self):
        return  str(self.position)

    def __eq__(self, other):
        return other.position == self.position and other.color == self.color

def parseToPawn(text):
    return Pawn("",int(text[1:]),text[0],0)
