import math
import gcore.globalvars as g
import gcore.units.position as position
import gcore.units.ghost as ghost



class Clyde(ghost.Ghost):
    def __init__(self):
        super(Clyde, self).__init__(g.Colors.ORANGE, g.EntityType.CLYDE)
        self.scatter_target.ModCoords(int(g.BLOCKSZ24/2), int(g.BLOCKSZ24*35 + g.BLOCKSZ24/2))
        self.home.ModCoords(int(g.BLOCKSZ24*15 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*17 + g.BLOCKSZ24/2))


    def CalculateTarget(self, mypac: position.Position):
        dist_x = float(abs(self.GetX() - mypac.GetX()))
        if dist_x > g.WND_W/2:
            dist_x = g.WND_W - dist_x
        dist = float(math.sqrt(math.pow(dist_x, 2) + math.pow(self.GetY() - mypac.GetY(), 2)))
        if dist > g.BLOCKSZ24*8:
            self.target.ModPos(mypac.GetPos())
        else:
            self.target.ModPos(self.scatter_target.GetPos())


    def UpdatePos(self, actual_board, mypac, timed_status):
        self.UpdateSpeed(mypac)
        self.UpdateStatus(mypac, timed_status)
        for i in range(0, self.GetSpeed()):
            self.UpdateFacing(mypac)
            if self.IsTargetToCalculate(mypac):
                self.CalculateTarget(mypac)
            self.CalculateDirection(actual_board)
            self.Move(self.GetDirection())
            self.CheckWrap()

