from .position import Position


class Pawn:

    position = ""
    color = ""

    def __init__(self, color,position, typeOfPisition):
        self.color = color
        self.position = Position(position,typeOfPisition)

    def __str__(self):
        return  str(self.position)

    def __eq__(self, other):
        return other.position == self.position and other.color == self.color

def parseToPawn(text):
    return Pawn("",int(text[1:]),text[0])
