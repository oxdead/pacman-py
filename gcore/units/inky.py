import gcore.globalvars as g
import gcore.units.position as position
import gcore.units.entity as entity
import gcore.units.ghost as ghost


class Inky(ghost.Ghost):

    def __init__(self):
        super(Inky, self).__init__(g.Colors.CYAN, g.EntityType.INKY)
        self.scatter_target.ModCoords(int(g.BLOCKSZ24*26 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*35 + g.BLOCKSZ24/2))
        self.home.ModCoords(int(g.BLOCKSZ24*11 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*17 + g.BLOCKSZ24/2))


    def CalculateTarget(self, mypac: entity.Entity, blinky_pos: position.Position):
        x = mypac.GetX()
        y = mypac.GetY()
        match mypac.GetDirection():
            case g.Direction.RIGHT:
                x += g.BLOCKSZ24*2
            case g.Direction.UP:
                y -= g.BLOCKSZ24*2
            case g.Direction.LEFT:
                x -= g.BLOCKSZ24*2
            case g.Direction.DOWN:
                y += g.BLOCKSZ24*2
        
        x1 = x - blinky_pos.GetX()
        y1 = y - blinky_pos.GetY()
        self.target.ModCoords(x + x1, y + y1)


    def UpdatePos(self, actual_board, mypac, blinky_pos, timed_status):
        self.UpdateSpeed(mypac)
        self.UpdateStatus(mypac, timed_status)
        for i in range(0, self.GetSpeed()):
            self.UpdateFacing(mypac)
            if self.IsTargetToCalculate(mypac):
                self.CalculateTarget(mypac, blinky_pos)
            self.CalculateDirection(actual_board)
            self.Move(self.GetDirection())
            self.CheckWrap()

