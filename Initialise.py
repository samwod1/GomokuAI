import pygame

# change these values
move_first = 'O'  # human 'X' and computer 'O'
board_size = 3  # set between 0 - 15
win_condition = 3  # how many stones you need in a row to win
ai_type = 'MinimaxAlphaBeta'  # choose from 'MCTS', 'SimpleMCTS', 'MinimaxAlphaBeta', and 'MinimaxRollout'.

# Dont edit values below this :)

pygame.init()

board = []
graphical_board = []

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
MARGIN = 5

FONT = pygame.font.Font("assets/Roboto-Regular.ttf", 100)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BOARD_SIZE = 405

pygame.display.set_caption("Gomoku")

X_IMG = pygame.image.load("assets/black stone.png")
X_IMG = pygame.transform.scale(X_IMG, (22, 22))

WINNER_IMG = pygame.image.load("assets/stone win.png")
WINNER_IMG = pygame.transform.scale(WINNER_IMG, (22, 22))

O_IMG = pygame.image.load("assets/white stone.png")
O_IMG = pygame.transform.scale(O_IMG, (22, 22))

BG_COLOR = (255, 253, 243)

distanceBtwRows = BOARD_SIZE // board_size

humanTurn = 'X'
computerTurn = 'O'
