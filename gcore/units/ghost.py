import math
import gcore.globalvars as g
import gcore.timer as timer
import gcore.ltexture as ltexture
import gcore.units.position as position
import gcore.units.entity as entity
import gcore.units.pac as pac


class Ghost(entity.Entity):
    def __init__(self, my_color, my_identity):
        super(Ghost, self).__init__(my_identity)
        self.__body = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_body32.png", color=my_color)
        self.__body_blue = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_body32.png", color=(0,0,255))
        self.__body_white = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_body32.png", color=(255,255,255))
        self.__cur_body_frame = 0 
        self.__eyes = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_eyes32.png")
        self.__eyes_red = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_eyes32.png", color=(255, 0, 0))
        self.__eyes_white = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "ghost_eyes32.png")
        self.__eyes_white.ReplaceColor((0, 9, 245) , (255, 255, 255))
        self.__can_use_doors = False
        self.__is_scattering = False # true: scattering around, false: chases the pac
        
        self.target = position.Position()
        self.scatter_target = position.Position()
        self.door_target = position.Position()
        self.door_target.ModCoords(g.BLOCKSZ24*13 + g.BLOCKSZ24/2, g.BLOCKSZ24*15)
        self.home = position.Position()


    def IsTargetToCalculate(self, mypac: pac.Pac) -> bool:
        if not self.IsAlive():
            self.__can_use_doors = True
            self.target.ModPos(self.home)
            if self.GetPos() == self.home.GetPos():
                self.ModLifeStatement(True)
            return False

        # prevent hiding at home, when pac is energized
        if self.IsHome() and mypac.IsEnergized():
            if self.GetPos() == self.home.GetPos():
                self.target.ModY(self.home.GetY() - g.BLOCKSZ24)
            elif self.GetX() == self.home.GetX() and self.GetY() == self.home.GetY() - g.BLOCKSZ24:
                self.target.ModY(self.home.GetY())
            return False

        if self.IsHome() and self.IsAlive():
            self.__can_use_doors = True
            self.target.ModPos(self.door_target)
            return False

        self.__can_use_doors = False
        if self.__is_scattering:
            self.target.ModPos(self.scatter_target)
            return False
        else:
            return True


    def PossDirsBubbleSort(self, distances, possible_directions):
        for i in range(0, len(distances)):
            for j in range(0, len(distances)):
                if distances[i] < distances[j]:
                    temp1 = distances[i]
                    distances[i] = distances[j]
                    distances[j] = temp1
                    temp2 = possible_directions[i]
                    possible_directions[i] = possible_directions[j]
                    possible_directions[j] = temp2


    def CalculateDirection(self, actual_map):
        distances = [] # float[]
        possible_directions = [] # uchar[]
        for i in range (g.Direction.RIGHT, g.Direction.DOWN + 1):
            x = self.GetX()
            y = self.GetY()
            x, y = self.GetPossiblePosition(x, y, i)
            if not self.WallCollision(x, y, actual_map, self.__can_use_doors):
                dist_x = float(abs(x - self.target.GetX()))
                if dist_x > (g.WND_W / 2.0):
                    dist_x = g.WND_W - dist_x
                dist = float(math.sqrt(math.pow(dist_x, 2) + math.pow(y - self.target.GetY(), 2)))
                distances.append(dist)
                possible_directions.append(i)

        if len(possible_directions) == 1:
            self.ModDirection(possible_directions[0])
            return

        self.PossDirsBubbleSort(distances, possible_directions)

        for i in range(0, len(possible_directions)):
            if possible_directions[i] != ((self.GetDirection() + 2) % 4):
                self.ModDirection(possible_directions[i])
                return


    def IsHome(self):
        return self.IsInsideRect(g.BLOCKSZ24*11, g.BLOCKSZ24*15, g.BLOCKSZ24*17, g.BLOCKSZ24*18)


    def ModStatus(self, new_status):
        self.__is_scattering = new_status

 
    def UpdateStatus(self, mypac: pac.Pac, timed_status):
        if mypac.IsEnergized():
            if not self.__is_scattering:
                self.__is_scattering = True
            return
        
        if timed_status:
            if not self.__is_scattering:
                self.__is_scattering = True
        else:
            if self.__is_scattering:
                self.__is_scattering = False


    def UpdateFacing(self, mypac: pac.Pac):
        if self.IsHome():
            if self.GetDirection() == g.Direction.DOWN:
                self.ModFacing(g.Facing.UP)
            else:
                self.ModFacing(g.Facing.DOWN)
            return
        
        if mypac.IsEnergized():
            if not self.IsAlive():
                self.ModFacing(self.GetDirection())
            else:
                self.ModFacing(g.Facing.GHOST_PREY) 
            return
        
        self.ModFacing(self.GetDirection())
        

    def UpdateSpeed(self, mypac: pac.Pac): 
        if not self.IsAlive() and self.GetSpeed() != 6:
            self.ModSpeed(6)
            return
        
        if mypac.IsEnergized():
            if self.GetSpeed() != 1:
                self.ModSpeed(1)
        else:
            if self.GetSpeed() != 2:
                self.ModSpeed(2)
        

    def Draw(self, mypac: pac.Pac, ghost_timer: timer.Timer, timer_target):
        # body: 0=default, 1=blue, 2=white
        # eyes: 0=default, 1=white, 2=red
        color_state = 0
        if mypac.IsEnergized() and self.IsAlive() and not self.IsHome():
            color_state = 1
            if ghost_timer.GetTicks() > timer_target - 2000:
                if (int(math.floor(ghost_timer.GetTicks() / 250))) % 2 == 1:
                    color_state = 2

        if self.IsAlive():
            if color_state == 1:
                self.__body_blue.RenderFrame(int(self.__cur_body_frame / self.__body_blue.GetSize()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)
            elif color_state == 2:
                self.__body_white.RenderFrame(int(self.__cur_body_frame / self.__body_white.GetSize()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)
            else:
                self.__body.RenderFrame(int(self.__cur_body_frame / self.__body.GetSize()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)

        if color_state == 1:
            self.__eyes_white.RenderFrame(int(self.GetFacing()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)
        elif color_state == 2:
            self.__eyes_red.RenderFrame(int(self.GetFacing()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)
        else:
            self.__eyes.RenderFrame(int(self.GetFacing()), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)

        self.__cur_body_frame += 1
        if int(self.__cur_body_frame / self.__body.GetSize()) >= self.__body.GetSize():
            self.__cur_body_frame = 0
