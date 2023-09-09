class Position:
    def __init__(self, x = 0, y = 0):
        self.__x = x
        self.__y = y


    def GetX(self):
        return self.__x


    def GetY(self):
        return self.__y


    def GetPos(self):
        my_pos = Position(self.__x, self.__y)
        return my_pos


    def ModX(self, new_x):
        self.__x = new_x


    def ModY(self, new_y):
        self.__y = new_y


    def ModCoords(self, new_x, new_y):
        self.__x = new_x
        self.__y = new_y


    def ModPos(self, new_pos):
        self.__x = new_pos.GetX()
        self.__y = new_pos.GetY()


    def IsInsideRect(self, left, top, right, bottom) -> bool:
        return ((self.__x > left) and (self.__x < right) and (self.__y > top) and (self.__y < bottom))


    def __eq__(self, other): # other: Position, overload operator == 
        return (self.__x == other.GetX() and self.__y == other.GetY())











