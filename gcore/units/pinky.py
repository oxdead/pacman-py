import gcore.globalvars as g
import gcore.units.entity as entity
import gcore.units.ghost as ghost


class Pinky(ghost.Ghost):
    def __init__(self):
        super(Pinky, self).__init__(g.Colors.PINK, g.EntityType.PINKY)
        self.scatter_target.ModCoords(int(g.BLOCKSZ24*2 + g.BLOCKSZ24/2), int(g.BLOCKSZ24/2))
        self.home.ModCoords(int(g.BLOCKSZ24*13 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*17 + g.BLOCKSZ24/2))


    def CalculateTarget(self, mypac: entity.Entity):
        x = mypac.GetX()
        y = mypac.GetY()
        match  mypac.GetDirection():
            case g.Direction.RIGHT:
                x += 4 * g.BLOCKSZ24
            case g.Direction.UP:
                y -= 4 * g.BLOCKSZ24
            case g.Direction.LEFT:
                x -= 4 * g.BLOCKSZ24
            case g.Direction.DOWN:
                y += 4 * g.BLOCKSZ24

        self.target.ModCoords(x, y)
    

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

