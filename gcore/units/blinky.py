
import gcore.globalvars as g
import gcore.units.position as position
import gcore.units.ghost as ghost


class Blinky(ghost.Ghost):
    def __init__(self):
        super(Blinky, self).__init__(g.Colors.RED, g.EntityType.BLINKY)
        self.scatter_target.ModCoords(int(g.BLOCKSZ24*25 + g.BLOCKSZ24/2), int(g.BLOCKSZ24/2))
        self.home.ModCoords(int(g.BLOCKSZ24*13 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*17 + g.BLOCKSZ24/2))


    def CalculateTarget(self, my_pac: position.Position):
        self.target.ModPos(my_pac.GetPos())


    def UpdatePos(self, actual_board, my_pac, timed_status):
        self.UpdateSpeed(my_pac)
        self.UpdateStatus(my_pac, timed_status)
        for i in range(0, self.GetSpeed()):
            self.UpdateFacing(my_pac)
            if self.IsTargetToCalculate(my_pac):
                self.CalculateTarget(my_pac)
            self.CalculateDirection(actual_board)
            self.Move(self.GetDirection())
            self.CheckWrap()

