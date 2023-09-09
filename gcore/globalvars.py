import pygame

window: pygame.Surface = None
font: pygame.font.Font = None
font_small: pygame.font.Font = None

BOARD_W = 28
BOARD_H = 36
BLOCKSZ24 = 24
BLOCKSZ32 = 32
WND_W = BOARD_W * BLOCKSZ24
WND_H = BOARD_H * BLOCKSZ24
FPS = 60


# multi-line '''str''' will not work here as it adds \n on each line
char_board = \
"                            " \
"                            " \
"                            " \
"############################" \
"#............##............#" \
"#.####.#####.##.#####.####.#" \
"#o####.#####.##.#####.####o#" \
"#.####.#####.##.#####.####.#" \
"#..........................#" \
"#.####.##.########.##.####.#" \
"#.####.##.########.##.####.#" \
"#......##....##....##......#" \
"######.##### ## #####.######" \
"     #.##### ## #####.#     " \
"     #.##    1     ##.#     " \
"     #.## ###==### ##.#     " \
"######.## #      # ##.######" \
"      .   #2 3 4 #   .      " \
"######.## #      # ##.######" \
"     #.## ######## ##.#     " \
"     #.##          ##.#     " \
"     #.## ######## ##.#     " \
"######.## ######## ##.######" \
"#............##............#" \
"#.####.#####.##.#####.####.#" \
"#.####.#####.##.#####.####.#" \
"#o..##.......0 .......##..o#" \
"###.##.##.########.##.##.###" \
"###.##.##.########.##.##.###" \
"#......##....##....##......#" \
"#.##########.##.##########.#" \
"#.##########.##.##########.#" \
"#..........................#" \
"############################" \
"                            " \
"                            " 


class Colors:
    BLACK =  (0x00, 0x00, 0x00)
    WHITE =  (0xff, 0xff, 0xff)
    YELLOW = (0xff, 0xff, 0x00)
    RED =    (0xff, 0x00, 0x00)
    CYAN =   (0x00, 192, 0xff)
    PINK =   (0xff, 192, 203)
    ORANGE = (0xff, 128, 0x00)


class BlockType:
    NOTHING, WALL, DOOR, PELLET, ENERGIZER = range(0, 5)


# GHOST_PREY is a face for ghosts only and activates when pac is energized
class Facing:
    RIGHT, DOWN, LEFT, UP, GHOST_PREY = range(0, 5)


class Direction:
    RIGHT, UP, LEFT, DOWN = range(0, 4)


class EntityType:
    NOONE, PACMAN, BLINKY, INKY, PINKY, CLYDE = range(0, 6)


