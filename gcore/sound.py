import os
import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.__intro        = pygame.mixer.Sound(os.path.join('sounds', 'intro.wav'))
        self.__eat_fruit     = pygame.mixer.Sound(os.path.join('sounds','eat_fruit.wav'))
        self.__extra_life    = pygame.mixer.Sound(os.path.join('sounds','extra_life.wav'))
        self.__pac_death     = pygame.mixer.Sound(os.path.join('sounds','pac_death.wav'))
        self.__ghost_death   = pygame.mixer.Sound(os.path.join('sounds','ghost_death.wav'))
        self.__scatter_ghost = pygame.mixer.Sound(os.path.join('sounds','scatter_ghost.wav'))
        self.__waka         = pygame.mixer.Sound(os.path.join('sounds','waka.wav'))
        self.__intro.set_volume(0.5)
        self.__eat_fruit.set_volume(0.5)    
        self.__extra_life.set_volume(0.5)   
        self.__pac_death.set_volume(0.5)    
        self.__ghost_death.set_volume(0.5)  
        self.__scatter_ghost.set_volume(0.5)
        self.__waka.set_volume(0.5)  
        
        # example how to play sounds through channels instead, for more fine control
        # if pygame.mixer.get_num_channels() > 1:
        #     self.__waka_channel = pygame.mixer.Channel(pygame.mixer.get_num_channels()-1)
        #     # usage: 
        #     # self.__waka_channel.play(sound=self.__waka, loops=-1)
        
        
    def __del__(self):
        pygame.mixer.quit()
        self.__intro = None
        self.__eat_fruit = None
        self.__extra_life = None
        self.__pac_death = None
        self.__ghost_death = None
        self.__scatter_ghost = None
        self.__waka = None


    def PlayIntro(self):
        self.__intro.play()
    

    def PlayEatFruit(self):
        self.__eat_fruit.play()
    

    def PlayExtraLife(self):
        self.__extra_life.play()
    

    def PlayPacDeath(self):
        self.__pac_death.play()
    

    def PlayGhostDeath(self):
        self.__ghost_death.play()
    

    def PlayScatterGhost(self):
        self.__scatter_ghost.play(loops=-1)
    

    def StopScatterGhost(self):
        self.__scatter_ghost.stop()
    

    def PlayWaka(self):
        self.__waka.play(loops=-1)
    
    
    def StopWaka(self):
        self.__waka.stop()