import pygame
import numpy as np

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

# board = [list(range(1, 10)), list(range(10, 19)), list(range(19, 28)), list(range(28, 37)), list(range(37, 46)),
#          list(range(46, 55)), list(range(55, 64)), list(range(64, 73)), list(range(73, 82))]

BG_COLOR = (255, 253, 243)
board_size = 4
game_finished = False
board = []
count = 0
for i in range(board_size):
    count += 1
    board.append([count])
    for j in range(board_size - 1):
        count += 1
        board[i].append(count)

print(board)

distanceBtwRows = BOARD_SIZE // board_size
winCondition = 3
humanTurn = 'X'
computerTurn = 'O'
move_first = 'X'