import pygame


class Timer:
    def __init__(self):
        self.__started = False
        self.__paused = False
        self.__start_ticks = 0 # ticks since start
        self.__paused_ticks = 0 # ticks since stop


    def Start(self):
        self.__started = True
        self.__paused = False
        self.__start_ticks = pygame.time.get_ticks()
        self.__paused_ticks = 0


    def Reset(self):
        self.__started = False
        self.__paused = False
        self.__start_ticks = 0
        self.__paused_ticks = 0


    def Restart(self):
        self.Reset()
        self.Start()


    def Pause(self):
        if self.__started and not self.__paused:
            self.__paused = True
            self.__paused_ticks = pygame.time.get_ticks() - self.__start_ticks
            self.__start_ticks = 0


    def Unpause(self):
        if self.__started and self.__paused:
            self.__paused = False
            self.__start_ticks = pygame.time.get_ticks() - self.__paused_ticks
            self.__paused_ticks = 0


    def GetTicks(self):
        time = 0
        if self.__started == True:
            if self.__paused == True:
                time = self.__paused_ticks
            else:
                time = pygame.time.get_ticks() - self.__start_ticks
        return time


    def IsStarted(self):
        return self.__started


        






