WIN_POSITION = "W"
START_POSITION = "S"
NORMAL_POSITION = "N"

class Position:

    number = ""
    typeOfPosition = ""

    def __init__(self,number,typeOfPosition):
        self.number = number
        self.typeOfPosition = typeOfPosition

    def __eq__(self, other):
        print(other)
        if type(other) == type(int())  or type(other) == type(str()):
            return int(self.number) == int(other) and self.typeOfPosition == other.typeOfPosition
        else:
            return int(self.number) == int(other.number) and self.typeOfPosition == other.typeOfPosition
    def __str__(self):
        return self.typeOfPosition+ str(self.number)