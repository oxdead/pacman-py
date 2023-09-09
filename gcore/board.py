import math
import gcore.globalvars as g
import gcore.timer as timer
import gcore.ltexture as ltexture
import gcore.units.entity as entity


class Board:
    def __init__(self):
        self.__map_texture_white = ltexture.LTexture("map24.png")
        self.__map_texture_blue = ltexture.LTexture("map24.png", color=(0x00, 0x00, 0xff))
        self.__pellet_texture = ltexture.LTexture("pellet24.png")
        self.__energizer_texture = ltexture.LTexture("energizer24.png")
        self.__door_texture = ltexture.LTexture("door.png")
        self.__lives_texture = ltexture.LTexture("lives32.png")
        self.__score_word_texture = ltexture.LTexture(texture_text="Score", color=g.Colors.WHITE)
        self.__score_texture = ltexture.LTexture(texture_text="0", color=g.Colors.WHITE)
        self.__score = 0
        self.__high_score_word_texture = ltexture.LTexture(texture_text="High Score", color=g.Colors.WHITE)
        self.__high_score_texture = ltexture.LTexture(texture_text="0", color=g.Colors.WHITE)
        self.__high_score = 0
        self.ReadHighScore()
        # self.__numeric_board = [None] * (g.BOARD_H * g.BOARD_W) # element values have the same address, do not init in this way, useless crap changes all elements on changing only 1 element
        self.__numeric_board = [None for i in range(g.BOARD_H * g.BOARD_W)]
        self.__is_extra = False
        self.__lives = 4
        self.ConvertSketch()


    def ConvertSketch(self):
        for i in range (0, g.BOARD_H * g.BOARD_W):
            match g.char_board[i]:
                case '#':
                    self.__numeric_board[i] = g.BlockType.WALL
                case '=':
                    self.__numeric_board[i] = g.BlockType.DOOR
                case '.':
                    self.__numeric_board[i] = g.BlockType.PELLET
                case 'o':
                    self.__numeric_board[i] = g.BlockType.ENERGIZER
                case _:
                    self.__numeric_board[i] = g.BlockType.NOTHING


    def CopyBoard(self, actual_map):
        for i in range(0, g.BOARD_H * g.BOARD_W):
            actual_map[i] = self.__numeric_board[i]


    def ResetPosition(self, some_entity: entity.Entity):
        y = 255
        for i in range(0, g.BOARD_H * g.BOARD_W):
            x = (i % g.BOARD_W)
            if x < 0: x = 0
            if x > 255: x = 255

            if x == 0: y += 1
            if y < 0: y = 0
            if y > 255: y = (y % 256) 

            if g.char_board[i] == '0' and some_entity.GetIdentity() == g.EntityType.PACMAN:
                some_entity.ModX(x * g.BLOCKSZ24 + g.BLOCKSZ24//2)
                some_entity.ModY(y * g.BLOCKSZ24)
                return
            elif g.char_board[i] == '1' and some_entity.GetIdentity() == g.EntityType.BLINKY:
                some_entity.ModX(x*g.BLOCKSZ24 + g.BLOCKSZ24//2)
                some_entity.ModY(y*g.BLOCKSZ24)
                return
            elif g.char_board[i] == '2' and some_entity.GetIdentity() == g.EntityType.INKY:
                some_entity.ModX(x*g.BLOCKSZ24 + g.BLOCKSZ24//2)
                some_entity.ModY(y*g.BLOCKSZ24)
                return
            elif g.char_board[i] == '3' and some_entity.GetIdentity() == g.EntityType.PINKY:
                some_entity.ModX(x*g.BLOCKSZ24 + g.BLOCKSZ24//2)
                some_entity.ModY(y*g.BLOCKSZ24)
                return
            elif g.char_board[i] == '4' and some_entity.GetIdentity() == g.EntityType.CLYDE:
                some_entity.ModX(x*g.BLOCKSZ24 + g.BLOCKSZ24//2)
                some_entity.ModY(y*g.BLOCKSZ24)
                return


    def SetScore(self):
        self.__score_texture = ltexture.LTexture(texture_text=str(self.__score), color=g.Colors.WHITE)


    def ReadHighScore(self):
        with open('high_score.txt') as f:
            high_scores = f.readlines()
            self.__high_score = int(high_scores[0] if high_scores[0] else '0')
        

    def SetHighScore(self):
        if self.__score > self.__high_score:
            self.__high_score = self.__score
            with open('high_score.txt', 'w') as f:
                f.write(str(self.__high_score))
        
        self.__high_score_texture = ltexture.LTexture(texture_text=str(self.__high_score), color=g.Colors.WHITE)


    def IsExtraLife(self):
        if not self.__is_extra and self.__score >= 10000:
            self.__is_extra = True
            self.__lives += 1
            return True
        return False


    def IncreaseLives(self):
        self.__lives += 1


    def DecreaseLives(self):
        self.__lives -= 1


    def GetLives(self):
        return self.__lives


    def ScoreIncrease(self, scorer):
        self.__score += scorer


    def Draw(self, actual_map, map_animation_timer: timer.Timer):
        if map_animation_timer.IsStarted() and (int(math.floor(map_animation_timer.GetTicks() / 250))) % 2 == 1:
            self.__map_texture_white.Render()
        else:
            self.__map_texture_blue.Render()

        self.__score_word_texture.Render()
        self.__score_texture.Render(0, g.BLOCKSZ32)
        self.__high_score_word_texture.Render(336)
        self.__high_score_texture.Render(336, g.BLOCKSZ32)

        for i in range (1, self.__lives + 1):
            self.__lives_texture.Render(int(g.BLOCKSZ32*i), int(g.BLOCKSZ32*26 - g.BLOCKSZ32/4))

        if not map_animation_timer.IsStarted():
            self.__door_texture.Render(int(g.WND_W/2 - 23), int(g.WND_H/2 - 57))
            y = 255
            for i in range (0, g.BOARD_H * g.BOARD_W):
                x = i % g.BOARD_W
                if x < 0: x = 0
                if x > 255: x = 255

                if x == 0: y += 1
                if y < 0: y = 0
                if y > 255: y = y % 256

                if actual_map[i] == g.BlockType.PELLET:
                    self.__pellet_texture.Render(int(g.BLOCKSZ24*x), int(g.BLOCKSZ24*y))
                if actual_map[i] == g.BlockType.ENERGIZER:
                    self.__energizer_texture.Render(int(g.BLOCKSZ24*x), int(g.BLOCKSZ24*y))


