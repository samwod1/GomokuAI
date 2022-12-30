import pygame
pygame.init()

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
MARGIN = 5

FONT = pygame.font.Font("assets/Roboto-Regular.ttf", 100)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BOARD_SIZE = 405

pygame.display.set_caption("Gomoku")

X_IMG = pygame.image.load("assets/black stone.png")
X_IMG = pygame.transform.scale(X_IMG, (22, 22))

X_WIN = pygame.image.load("assets/stone win.png")
X_WIN = pygame.transform.scale(X_WIN, (22, 22))

O_IMG = pygame.image.load("assets/white stone.png")
O_IMG = pygame.transform.scale(O_IMG, (22, 22))

O_WIN = pygame.image.load("assets/stone win.png")
O_WIN = pygame.transform.scale(O_WIN, (22, 22))

board = [list(range(1, 16)), list(range(16, 31)), list(range(31, 46)), list(range(46, 61)),
         list(range(61, 76)),
         list(range(76, 91)), list(range(91, 106)), list(range(106, 121)), list(range(121, 136)),
         list(range(136, 151)),
         list(range(151, 166)), list(range(166, 181)), list(range(181, 196)), list(range(196, 211)),
         list(range(211, 226))]

BG_COLOR = (255, 253, 243)
board_size = 15
game_finished = False
