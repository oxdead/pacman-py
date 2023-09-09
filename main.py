
import os
import sys
import pygame
import gcore.globalvars as g
import gcore.timer
import gcore.game


def Main():

    g.window = pygame.display.set_mode((g.WND_W, g.WND_H), vsync=0)
    pygame.display.set_caption("Pac-Man")

    pygame.font.init()
    g.font = pygame.font.Font(os.path.join("fonts", 'emulogic.ttf'), g.BLOCKSZ24)
    g.font_small = pygame.font.Font(os.path.join("fonts", 'vppixel.ttf'), 20)

    game_obj = gcore.game.Game()
    game_obj.StartMainTimer()
    game_obj.s_sound.PlayIntro()
    mover = []
    mover.append(g.Direction.RIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(g.FPS)
        # print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    mover.append(g.Direction.RIGHT)
                if (event.key == pygame.K_UP or event.key == pygame.K_w):
                    mover.append(g.Direction.UP)
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    mover.append(g.Direction.LEFT)
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    mover.append(g.Direction.DOWN)
                if len(mover) > 2:
                    mover.pop(1)

        game_rv = game_obj.Process(mover)
        if game_rv:
            game_obj.Draw()
        pygame.display.update()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(Main())
	



