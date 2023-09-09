
import gcore.globalvars as g
import gcore.ltexture as ltexture
import gcore.timer as timer
import gcore.sound as sound
import gcore.board as board

import gcore.units.position as position
import gcore.units.pac as pac
import gcore.units.ghost as ghost
import gcore.units.blinky as blinky
import gcore.units.inky as inky
import gcore.units.pinky as pinky
import gcore.units.clyde as clyde
import gcore.units.fruit as fruit


class Game:
    
    s_sound = None # static public class attribute

    def __init__(self):
        self.__start_ticks = 4500
        self.__main_timer = timer.Timer()
        self.__actual_map = [None for i in range(g.BOARD_H * g.BOARD_W)]
        self.__board = board.Board()
        self.__board.CopyBoard(self.__actual_map)
        self.__pac = pac.Pac()
        self.__blinky = blinky.Blinky()
        self.__blinky_go = self.__start_ticks
        self.__inky = inky.Inky()
        self.__inky_go = self.__start_ticks + 1000
        self.__pinky = pinky.Pinky()
        self.__pinky_go = self.__start_ticks + 3000
        self.__clyde = clyde.Clyde()
        self.__clyde_go = self.__start_ticks + 5000
        self.__fruit = fruit.Fruit()
        self.__map_animation_timer = timer.Timer()
        self.__ready = ltexture.LTexture(texture_text="ready!", color=g.Colors.YELLOW)
        self.__game_over_texture = ltexture.LTexture(texture_text="game  over", color=g.Colors.RED)
        self.__is_game_started = False
        self.__ghost_timer = timer.Timer() # needed to calc the time oto change state when pac is energized and not
        self.__scatter_time = 7000
        self.__chasing_time = 20000
        self.__ghost_timer_target = self.__chasing_time
        self.__timed_status = False
        self.__scorer = 200
        self.__positional_score = {"scorers": [], "positions": [], "timers": []}
        self.__level = 1
        self.__is_scatter_sound = True
        self.__is_waka_sound = True
        self.__waka_timer = timer.Timer()
        self.__is_death_pac_sound = True
        self.__dead_ghosts_counter = 0
        self.s_sound = sound.Sound()
        

    def ResetGhostsLifeStatement(self):
        self.__blinky.ModLifeStatement(True)
        self.__inky.ModLifeStatement(True)
        self.__pinky.ModLifeStatement(True)
        self.__clyde.ModLifeStatement(True)


    def ResetGhostsFacing(self):
        self.__blinky.ModFacing(g.Facing.RIGHT)
        self.__inky.ModFacing(g.Facing.DOWN)
        self.__pinky.ModFacing(g.Facing.DOWN)
        self.__clyde.ModFacing(g.Facing.DOWN)


    def StartMainTimer(self):
        self.__main_timer.Start()


    def Start(self):
        if not self.__is_game_started:
            if self.IsLevelCompleted():
                self.__board.CopyBoard(self.__actual_map)

            self.__board.ResetPosition(self.__pac)
            self.__board.ResetPosition(self.__blinky)
            self.__board.ResetPosition(self.__inky)
            self.__board.ResetPosition(self.__pinky)
            self.__board.ResetPosition(self.__clyde)
            self.__pac.ChangeEnergyStatus(False)
            self.ResetGhostsLifeStatement()
            self.ResetGhostsFacing()
            self.__pac.ResetCurrentLivingFrame()
            self.__ghost_timer.Restart()
            self.__is_game_started = True
            self.__ghost_timer.Start()


    def ModStartStatement(self, new_start_statement):
        self.__is_game_started = new_start_statement


    def Clock(self):
        if self.__ghost_timer.GetTicks() > self.__ghost_timer_target:
            if self.__ghost_timer_target == self.__scatter_time:
                if self.__pac.IsEnergized():
                    self.__pac.ChangeEnergyStatus(False)

                self.__timed_status = False
                self.__ghost_timer_target = self.__chasing_time
                self.__ghost_timer.Restart()

            elif self.__ghost_timer_target == self.__chasing_time:
                self.__timed_status = True
                self.__ghost_timer_target = self.__scatter_time
                self.__ghost_timer.Restart()


    def UpdateGhostsRelease(self):
        self.__blinky_go = self.__start_ticks
        self.__inky_go = self.__start_ticks + 1000
        self.__pinky_go = self.__start_ticks + 3000
        self.__clyde_go = self.__start_ticks + 5000


    def UpdatePositions(self, mover, timed_status):
        if self.__main_timer.GetTicks() > self.__blinky_go:
            self.__blinky.UpdatePos(self.__actual_map, self.__pac, timed_status)
        if self.__main_timer.GetTicks() > self.__inky_go:
            self.__inky.UpdatePos(self.__actual_map, self.__pac, self.__blinky, timed_status)
        if self.__main_timer.GetTicks() > self.__pinky_go:
            self.__pinky.UpdatePos(self.__actual_map, self.__pac, timed_status)
        if self.__main_timer.GetTicks() > self.__clyde_go:
            self.__clyde.UpdatePos(self.__actual_map, self.__pac, timed_status)
        self.__pac.UpdatePos(mover, self.__actual_map);	


    def Food(self):
        match self.__pac.FoodCollision(self.__actual_map):
            case 0:
                self.__board.ScoreIncrease(10)
                self.__fruit.UpdateFoodCounter()
                if self.__is_waka_sound:
                    self.s_sound.PlayWaka()
                    self.__is_waka_sound = False
                self.__waka_timer.Reset()
            case 1:
                self.__board.ScoreIncrease(50)
                self.__fruit.UpdateFoodCounter()
                self.__pac.ChangeEnergyStatus(True)
                self.__scorer = 200
                self.__ghost_timer_target = self.__scatter_time
                self.__ghost_timer.Restart()
                if self.__is_waka_sound:
                    self.s_sound.PlayWaka()
                    self.__is_waka_sound = False
                self.__waka_timer.Reset()
            case _:
                if not self.__waka_timer.IsStarted():
                    self.__waka_timer.Start()

        if self.__waka_timer.GetTicks() > 300:
            self.s_sound.StopWaka()
            self.__is_waka_sound = True


    def EntityCollisions(self):
        if not self.__pac.IsEnergized():
            self.GhostEatsPac()
            if not self.__is_scatter_sound:
                self.__dead_ghosts_counter = 0
                self.s_sound.StopScatterGhost()
                self.__is_scatter_sound = True
        else:
            if self.__is_scatter_sound:
                self.s_sound.PlayScatterGhost()
                self.__is_scatter_sound = False
            self.PacEatsGhosts(self.__blinky)
            self.PacEatsGhosts(self.__inky)
            self.PacEatsGhosts(self.__pinky)
            self.PacEatsGhosts(self.__clyde)
            if self.__dead_ghosts_counter == 4:
                if not self.__is_scatter_sound:
                    self.s_sound.StopScatterGhost()

        if self.__fruit.IsEatable():
            if self.__pac.IsColliding(self.__fruit):
                self.__fruit.StartScoreTimer()
                self.__board.ScoreIncrease(self.__fruit.GetScoreValue())
                self.__fruit.Despawn()
                self.s_sound.PlayEatFruit()
            else:
                if self.__fruit.CheckDespawn():
                    self.__fruit.Despawn()


    def Update(self, mover):
        self.Clock()
        self.UpdatePositions(mover, self.__timed_status)
        self.Food()
        if self.__board.IsExtraLife():
            self.s_sound.PlayExtraLife()
        self.EntityCollisions()


    def GetLevel(self):
        return self.__level


    def IncreaseLevel(self):
        self.__level += 1


    def UpdateDifficulty(self):
        if self.__level % 3 == 0:
            self.__chasing_time += 1000
            if self.__scatter_time > 2000:
                self.__scatter_time -= 1000


    def IsLevelCompleted(self):
        for i in range(0, g.BOARD_H * g.BOARD_W):
            if self.__actual_map[i] == g.BlockType.PELLET:
                return False
            if self.__actual_map[i] == g.BlockType.ENERGIZER:
                return False
        return True


    def ClearMover(self, mover: list):
        while len(mover) > 0:
            mover.pop(0)
        mover.append(g.Direction.RIGHT)


    def GhostEatsPac(self):
        if (
            (self.__pac.IsColliding(self.__blinky) and self.__blinky.IsAlive()) 
            or (self.__pac.IsColliding(self.__inky) and self.__inky.IsAlive()) 
            or (self.__pac.IsColliding(self.__pinky) and self.__pinky.IsAlive()) 
            or (self.__pac.IsColliding(self.__clyde) and self.__clyde.IsAlive())
        ):
            self.__pac.ModLifeStatement(False)


    def PacEatsGhosts(self, ighost: ghost.Ghost):
        if self.__pac.IsColliding(ighost) and ighost.IsAlive():
            ighost.ModLifeStatement(False)
            
            self.__board.ScoreIncrease(self.__scorer)
            self.__positional_score.get("scorers").append(self.__scorer)
            lilpos = position.Position()
            lilpos.ModPos(ighost.GetPos())
            self.__positional_score.get("positions").append(lilpos)
            ghost_liltimer = timer.Timer()
            ghost_liltimer.Start()
            self.__positional_score.get("timers").append(ghost_liltimer)

            self.__scorer *= 2
            self.s_sound.PlayGhostDeath()
            self.__dead_ghosts_counter += 1


    def DeathSound(self):
        if self.__is_death_pac_sound:
            self.s_sound.StopWaka()
            self.s_sound.PlayPacDeath()
            self.__is_death_pac_sound = False


    def ModDeathSoundStatement(self, new_death_sound_statement):
        self.__is_death_pac_sound = new_death_sound_statement


    def DrawPositionalLittleScore(self):
        i = 0
        while i < len(self.__positional_score.get("timers")):
            liltimer: timer.Timer = self.__positional_score.get("timers")[i]
            if liltimer.GetTicks() < 1000:
                lilpos: position.Position = self.__positional_score.get("positions")[i]
                liltexture = ltexture.LTexture(texture_text=str(self.__positional_score.get("scorers")[i]), color=g.Colors.WHITE, is_small_font=True)
                liltexture.Render(int(lilpos.GetX()), int(lilpos.GetY() - g.BLOCKSZ24/2))
                i += 1
            else:
                self.__positional_score.get("scorers").pop(i)
                self.__positional_score.get("timers").pop(i)
                self.__positional_score.get("positions").pop(i)


    # returns false when should render the last animation frame. it's bad looking, so I don't want to render it.
    def Process(self, mover):
        if self.__main_timer.GetTicks() < self.__start_ticks:
            # runs only at starting the game/map
            self.Start()
        else:
            if self.__pac.IsAlive():
                
                if not self.IsLevelCompleted():
                    # runs on every tick
                    self.Update(mover)
                else:
                    # if level was finished, clear and regen
                    if not self.__map_animation_timer.IsStarted():
                        if self.__start_ticks != 2500:
                            self.__start_ticks = 2500
                            self.UpdateGhostsRelease()
                        self.__pac.ResetCurrentLivingFrame()
                        self.__fruit.Despawn()
                        self.__fruit.ResetFoodCounter()
                        self.__is_waka_sound = True
                        self.s_sound.StopWaka()
                        self.s_sound.StopScatterGhost()
                        self.__map_animation_timer.Start()
                    elif self.__map_animation_timer.GetTicks() > 2100:
                        self.ClearMover(mover)
                        self.IncreaseLevel()
                        self.__fruit.ModCurrentFruit(self.GetLevel())
                        self.UpdateDifficulty()
                        self.ModStartStatement(False)
                        self.__map_animation_timer.Reset()
                        self.__main_timer.Start()
                        return False
            else:
                if self.__board.GetLives() > 0:
                    if self.__pac.IsDeadAnimationEnded():
                        if self.__start_ticks != 2500:
                            self.__start_ticks = 2500
                            self.UpdateGhostsRelease()
                        self.ClearMover(mover)
                        self.__pac.ModDeadAnimationStatement(False)
                        self.__pac.ModLifeStatement(True)
                        self.__board.DecreaseLives()
                        self.__fruit.Despawn()
                        self.__is_waka_sound = True
                        self.ModDeathSoundStatement(True)
                        self.ModStartStatement(False)
                        self.__main_timer.Restart()
                        return False
                else:
                    if self.__pac.IsDeadAnimationEnded():
                        self.ModStartStatement(False)
                self.DeathSound()
        return True


    def Draw(self):
        g.window.fill(g.Colors.BLACK)
        self.__board.SetScore()
        self.__board.SetHighScore()
        self.__board.Draw(self.__actual_map, self.__map_animation_timer)

        if self.__main_timer.GetTicks() < self.__start_ticks:
            self.__ready.Render(int(g.BLOCKSZ24*11), int(g.BLOCKSZ24*20 - 5))
        elif not self.__is_game_started:
            self.__game_over_texture.Render(int(g.BLOCKSZ24*9), int(g.BLOCKSZ24*20 - 5))
            return
        
        self.__fruit.Draw()

        if not self.__map_animation_timer.IsStarted():
            self.__clyde.Draw(self.__pac, self.__ghost_timer, self.__scatter_time)
            self.__pinky.Draw(self.__pac, self.__ghost_timer, self.__scatter_time)
            self.__inky.Draw(self.__pac, self.__ghost_timer, self.__scatter_time)
            self.__blinky.Draw(self.__pac, self.__ghost_timer, self.__scatter_time)
            self.DrawPositionalLittleScore()

        self.__pac.Draw()



