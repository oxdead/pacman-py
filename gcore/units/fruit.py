import math
import gcore.globalvars as g
import gcore.units.position as position
import gcore.ltexture as ltexture
import gcore.timer as timer


class Fruit(position.Position):
    def __init__(self):
        self.__fruit_texture = ltexture.LTextureFrames(g.BLOCKSZ32, g.BLOCKSZ32, True, "fruit32.png")
        self.__current_fruit = 0
        self.__fruit_timer = timer.Timer()
        self.__score_timer = timer.Timer()
        self.__score_table = [100, 300, 500, 700, 1000, 2000, 3000, 5000] # FruitFrames = 8
        self.ModCoords(int(g.BLOCKSZ24*13 + g.BLOCKSZ24/2), int(g.BLOCKSZ24*20))
        self.__fruit_duration = 9000
        self.__food_counter = 0
        

    def ModCurrentFruit(self, actual_level):
        if actual_level > 21:
            if self.__current_fruit != 7:
                self.__current_fruit = 7
        else:
            self.__current_fruit = int(math.floor((actual_level - 1)/3.0))


    def UpdateFoodCounter(self):
        self.__food_counter += 1
        if self.__food_counter == 70 or self.__food_counter == 200:
            if not self.__fruit_timer.IsStarted():
                self.__fruit_timer.Start()


    def IsEatable(self):
        if self.__fruit_timer.IsStarted():
            return True
        return False


    def GetScoreValue(self):
        return self.__score_table[int(self.__current_fruit)]


    def StartScoreTimer(self):
        self.__score_timer.Start()


    def ResetScoreTimer(self):
        if self.__score_timer.GetTicks() > 1000:
            self.__score_timer.Reset()


    def CheckDespawn(self):
        if self.__fruit_timer.GetTicks() > self.__fruit_duration:
            return True
        return False


    def Despawn(self):
        self.__fruit_timer.Reset()


    def ResetFoodCounter(self):
        self.__food_counter = 0


    def Draw(self):
        if self.__fruit_timer.IsStarted():
            self.__fruit_texture.RenderFrame(int(self.__current_fruit), int(self.GetX() - 4), int(self.GetY() - 4), 0.0)

        if self.__score_timer.IsStarted() and self.__score_timer.GetTicks() < 1000:
            score_texture = ltexture.LTexture(texture_text=str(self.__score_table[self.__current_fruit]), color=g.Colors.WHITE, is_small_font=True)
            score_texture.Render(int(self.GetX()), int(self.GetY() - g.BLOCKSZ24/2))

