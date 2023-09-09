
import gcore.globalvars as g
import gcore.ltexture as ltexture
import gcore.units.position as position
import gcore.units.entity as entity

class Pac(entity.Entity):
    def __init__(self):
        super(Pac, self).__init__(g.EntityType.PACMAN)
        self.__living_pac = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "pacman32.png")
        self.__cur_living_pac_frame = 0
        self.__dead_pac = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "game_over32.png")
        self.__cur_dead_pac_frame = 0
        self.__energy_status = False
        self.__dead_animation_statement = False

    
    def UpdatePos(self, mover: list, actual_map):
        for i in range(0, self.GetSpeed()):
            temp_x = self.GetX()
            temp_y = self.GetY()
            temp_x, temp_y = self.GetPossiblePosition(temp_x, temp_y, mover[0])
            if not self.WallCollision(temp_x, temp_y, actual_map):
                self.UpdateCurrentLivingPacFrame()
                self.Move(mover[0])
                self.SetFacing(mover[0])
                self.ModDirection(mover[0])
            else:
                self.WallCollisionFrame()

            if len(mover) != 1 and mover[0] != mover[1]:
                temp_x = self.GetX()
                temp_y = self.GetY()
                temp_x, temp_y = self.GetPossiblePosition(temp_x, temp_y, mover[1])
                if not self.WallCollision(temp_x, temp_y, actual_map):
                    self.UpdateCurrentLivingPacFrame()
                    self.Move(mover[1])
                    self.SetFacing(mover[1])
                    self.ModDirection(mover[1])
                    mover.pop(0)
            self.CheckWrap()


    def FoodCollision(self, actual_map):
        cell_x = float(float(self.GetX()) / float(g.BLOCKSZ24))
        cell_y = float(float(self.GetY()) / float(g.BLOCKSZ24))
        board_pos = position.Position()
        for side_dir in range(0, 4):
            self.CharBoardPos(side_dir, board_pos, cell_x, cell_y)
            if actual_map[g.BOARD_W * board_pos.GetY() + board_pos.GetX()] == g.BlockType.PELLET:
                actual_map[g.BOARD_W * board_pos.GetY() + board_pos.GetX()] = g.BlockType.NOTHING
                return 0
            elif actual_map[g.BOARD_W * board_pos.GetY() + board_pos.GetX()] == g.BlockType.ENERGIZER:
                actual_map[g.BOARD_W * board_pos.GetY() + board_pos.GetX()] = g.BlockType.NOTHING
                return 1
        return 2


    def IsEnergized(self):
        return self.__energy_status


    def ChangeEnergyStatus(self, new_energy_status):
        self.__energy_status = new_energy_status


    def SetFacing(self, mover_element):
        match mover_element:
            case g.Direction.RIGHT:
                self.ModFacing(g.Facing.RIGHT)
            case g.Direction.UP:
                self.ModFacing(g.Facing.DOWN)
            case g.Direction.LEFT:
                self.ModFacing(g.Facing.LEFT)
            case g.Direction.DOWN:
                self.ModFacing(g.Facing.UP)
            case _:
                pass


    def IsDeadAnimationEnded(self):
        return self.__dead_animation_statement


    def ModDeadAnimationStatement(self, new_dead_animation_statement):
        self.__dead_animation_statement = new_dead_animation_statement


    def UpdateCurrentLivingPacFrame(self):
        self.__cur_living_pac_frame += 1
        if int(self.__cur_living_pac_frame / (self.__living_pac.GetSize() * 4)) >= self.__living_pac.GetSize():
            self.__cur_living_pac_frame = 0


    def ResetCurrentLivingFrame(self):
        self.__cur_living_pac_frame = 0


    def WallCollisionFrame(self):
        self.__cur_living_pac_frame = 32


    def Draw(self):
        if self.IsAlive():
            self.__living_pac.RenderFrame(int(self.__cur_living_pac_frame / (self.__living_pac.GetSize() * 4)), int(self.GetX() - 4), int(self.GetY() - 4), self.GetFacing())
        else:
            self.__dead_pac.RenderFrame(int(self.__cur_dead_pac_frame / self.__dead_pac.GetSize()), int(self.GetX() - 4), int(self.GetY() - 4), self.GetFacing())
            
            self.__cur_dead_pac_frame += 1
            if (self.__cur_dead_pac_frame / self.__dead_pac.GetSize()) >= self.__dead_pac.GetSize():
                self.__dead_animation_statement = True
                self.__cur_dead_pac_frame = 0

