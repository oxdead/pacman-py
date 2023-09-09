import math
import gcore.globalvars as g
import gcore.units.position as position

class Entity(position.Position):
    def __init__(self, my_identity: g.EntityType):
        self.__identity = my_identity
        self.__speed = 2
        self.__direction = g.Direction.RIGHT
        self.__facing = g.Facing.RIGHT
        self.__life_statement = True


    def GetIdentity(self):
        return self.__identity


    def GetSpeed(self):
        return self.__speed


    def GetDirection(self):
        return self.__direction


    def GetFacing(self):
        return self.__facing


    def IsAlive(self):
        return self.__life_statement


    def ModSpeed(self, new_speed):
        self.__speed = new_speed


    def ModDirection(self, new_direction):
        self.__direction = new_direction


    def ModFacing(self, new_facing):
        self.__facing = new_facing


    def ModLifeStatement(self, new_life_statement):
        self.__life_statement = new_life_statement


    def GetPossiblePosition(self, x, y, mover_element):
        match mover_element:
            case g.Direction.RIGHT:
                x += 1
            case g.Direction.UP:
                y -= 1
            case g.Direction.LEFT:
                x -= 1
            case g.Direction.DOWN:
                y += 1
            case _:
                pass
                
        return x, y
        

    def CharBoardPos(self, side_dir, board_pos: position.Position, cell_x, cell_y):
        match side_dir:
            case 0:
                board_pos.ModX(int(math.floor(cell_x)))
                board_pos.ModY(int(math.floor(cell_y)))
            case 1:
                board_pos.ModX(int(math.ceil(cell_x)))
                board_pos.ModY(int(math.floor(cell_y)))
            case 2:
                board_pos.ModX(int(math.floor(cell_x)))
                board_pos.ModY(int(math.ceil(cell_y)))
            case 3:
                board_pos.ModX(int(math.ceil(cell_x)))
                board_pos.ModY(int(math.ceil(cell_y)))


    def WallCollision(self, x, y, actual_map, can_use_doors = False):
        cell_x = x / float(g.BLOCKSZ24)
        cell_y = y / float(g.BLOCKSZ24)
        board_pos = position.Position()

        for side_dir in range(0, 4):
            self.CharBoardPos(side_dir, board_pos, cell_x, cell_y)

            if actual_map[int(g.BOARD_W * board_pos.GetY() + abs(board_pos.GetX() % g.BOARD_W))] == g.BlockType.WALL:
                return True
            elif actual_map[int(g.BOARD_W * board_pos.GetY() + abs(board_pos.GetX() % g.BOARD_W))] == g.BlockType.DOOR:
                return not can_use_doors
            
        return False


    def Move(self, mover_element):
        match mover_element:
            case g.Direction.RIGHT:
                self.ModX(self.GetX() + 1)
            case g.Direction.UP:
                self.ModY(self.GetY() - 1)
            case g.Direction.LEFT:
                self.ModX(self.GetX() - 1)
            case g.Direction.DOWN:
                self.ModY(self.GetY() + 1)
            case _:
                pass


    def CheckWrap(self):
        if self.GetX() > g.WND_W + g.BLOCKSZ24:
            self.ModX(-(g.BLOCKSZ24))
        if self.GetX() < (-(g.BLOCKSZ24)):
            self.ModX(g.WND_W + g.BLOCKSZ24)


    def IsColliding(self, other: position.Position): 
        if (other.GetX() > self.GetX() - g.BLOCKSZ24) and (other.GetX() < self.GetX() + g.BLOCKSZ24):
            if (other.GetY() > self.GetY() - g.BLOCKSZ24) and (other.GetY() < self.GetY() + g.BLOCKSZ24):
                return True
        return False

