import sys
import pygame
import AI
from initialise import *

pygame.init()

def get_board_size():
    return board_size


def grid(SCREEN, size, board_size):
    distanceBtwRows = size // board_size
    x = 100
    y = 100

    pygame.draw.line(SCREEN, (0, 0, 0), (x, 100), (x, size + 100))
    pygame.draw.line(SCREEN, (0, 0, 0), (100, y), (size + 100, y))

    for i in range(15):
        x += distanceBtwRows
        y += distanceBtwRows
        pygame.draw.line(SCREEN, (0, 0, 0), (x, 100), (x, size + 100))
        pygame.draw.line(SCREEN, (0, 0, 0), (100, y), (size + 100, y))


def redraw():
    global SCREEN, WIDTH, board_size

    grid(SCREEN, BOARD_SIZE, board_size)
    pygame.display.update()


def reset_board():
    global graphical_board, board, to_move, game_finished

    board = [list(range(1, 16)), list(range(16, 31)), list(range(31, 46)), list(range(46, 61)),
             list(range(61, 76)),
             list(range(76, 91)), list(range(91, 106)), list(range(106, 121)), list(range(121, 136)),
             list(range(136, 151)),
             list(range(151, 166)), list(range(166, 181)), list(range(181, 196)), list(range(196, 211)),
             list(range(211, 226))]

    graphical_board = []
    for i in range(board_size):
        graphical_board.append([])
        for j in range(board_size):
            graphical_board[i].append([None, None])

    to_move = 'X'

    SCREEN.fill(BG_COLOR)
    pygame.display.flip()

    game_finished = False

    redraw()

    pygame.display.update()


def render_board(board, X_IMG, O_IMG):
    global graphical_board
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = X_IMG
                graphical_board[i][j][1] = X_IMG.get_rect(center=(j * 27 + 114, i * 27 + 114))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = O_IMG
                graphical_board[i][j][1] = O_IMG.get_rect(center=(j * 27 + 114, i * 27 + 114))


def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = round((current_pos[0] - 114) / 27)  # muck about with these values
    converted_y = round((current_pos[1] - 114) / 27)

    if (board_size - 1) >= converted_y >= 0 and (board_size - 1) >= converted_x >= 0:

        if board[converted_y][converted_x] != 'O' and board[converted_y][converted_x] != 'X':
            board[converted_y][converted_x] = to_move
            if to_move == 'X':
                to_move = 'O'
            else:
                to_move = 'X'

        render_board(board, X_IMG, O_IMG)

        for i in range(board_size):
            for j in range(board_size):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

    return board, to_move

def check_win_2(current_board):
    dim = board_size

    winner_found = False
    while not winner_found:
        # checks all horizontal wins
        winner = None
        for i in range(dim):
            for j in range(dim - 5):
                if current_board[i][j] == current_board[i][j + 1] == current_board[i][j + 2] == current_board[i][
                    j + 3] == current_board[i][j + 4]:

                    winner = current_board[i][j]

                    winnerImg = None

                    if (winner == 'X'):
                        winnerImg = X_WIN
                    else:
                        winnerImg = O_WIN

                    if winnerImg is not None:
                        graphical_board[i][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                        graphical_board[i][j + 1][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j + 1][0], graphical_board[i][j + 1][1])
                        graphical_board[i][j + 2][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j + 2][0], graphical_board[i][j + 2][1])
                        graphical_board[i][j + 3][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j + 3][0], graphical_board[i][j + 3][1])
                        graphical_board[i][j + 4][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j + 4][0], graphical_board[i][j + 4][1])
                        pygame.display.update()

        # checks vertical wins
        for i in range(dim - 5):
            for j in range(dim):
                if current_board[i][j] == current_board[i + 1][j] == current_board[i + 2][j] == current_board[i + 3][
                    j] == current_board[i + 4][j]:
                    winner = current_board[i][j]

                    winnerImg = None

                    if (winner == 'X'):
                        winnerImg = X_WIN
                    else:
                        winnerImg = O_WIN

                    if winnerImg is not None:
                        graphical_board[i][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                        graphical_board[i + 1][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i + 1][j][0], graphical_board[i + 1][j][1])
                        graphical_board[i + 2][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i + 2][j][0], graphical_board[i + 2][j][1])
                        graphical_board[i + 3][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i + 3][j][0], graphical_board[i + 3][j][1])
                        graphical_board[i + 4][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i + 4][j][0], graphical_board[i + 4][j][1])
                        pygame.display.update()

        # checks diagonal wins
        i = 4
        while i < board_size:
            j = 0
            while j < board_size - 4:
                if current_board[i][j] == current_board[i - 1][j + 1] == current_board[i - 2][j + 2] == \
                        current_board[i - 3][j + 3] == current_board[i - 4][j + 4]:
                    winner = current_board[i][j]

                    winnerImg = None

                    if winner == 'X':
                        winnerImg = X_WIN
                    else:
                        winnerImg = O_WIN

                    if winnerImg is not None:
                        graphical_board[i][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                        graphical_board[i - 1][j + 1][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 1][j + 1][0], graphical_board[i - 1][j + 1][1])
                        graphical_board[i - 2][j + 2][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 2][j + 2][0], graphical_board[i - 2][j + 2][1])
                        graphical_board[i - 3][j + 3][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 3][j + 3][0], graphical_board[i - 3][j + 3][1])
                        graphical_board[i - 4][j + 4][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 4][j + 4][0], graphical_board[i - 4][j + 4][1])
                        pygame.display.update()
                j += 1
            i += 1

        # checks other diagonals
        i = 4
        while i < board_size:
            j = 4
            while j < board_size:
                if current_board[i][j] == current_board[i - 1][j - 1] == current_board[i - 2][j - 2] == \
                        current_board[i - 3][j - 3] == current_board[i - 4][j - 4]:
                    winner = current_board[i][j]

                    winnerImg = None

                    if winner == 'X':
                        winnerImg = X_WIN
                    else:
                        winnerImg = O_WIN

                    if winnerImg is not None:
                        graphical_board[i][j][0] = winnerImg
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                        graphical_board[i - 1][j - 1][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 1][j - 1][0], graphical_board[i - 1][j - 1][1])
                        graphical_board[i - 2][j - 2][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 2][j - 2][0], graphical_board[i - 2][j - 2][1])
                        graphical_board[i - 3][j - 3][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 3][j - 3][0], graphical_board[i - 3][j - 3][1])
                        graphical_board[i - 4][j - 4][0] = winnerImg
                        SCREEN.blit(graphical_board[i - 4][j - 4][0], graphical_board[i - 4][j - 4][1])
                        pygame.display.update()
                j += 1
            i += 1

        if winner is None:
            for i in range(len(current_board)):
                for j in range(len(current_board)):
                    if current_board[i][j] != 'X' and current_board[i][j] != 'O':
                        return None
            return "DRAW"

        break

    return winner


def game_loop():
    global board, board_size, graphical_board, to_move, game_finished
    while True:
        for event in pygame.event.get():
            pygame.display.update() #updates display after the program hangs - which is quite often -
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                board, to_move = add_XO(board, graphical_board, to_move)

                if game_finished:
                    reset_board()

                if check_win_2(board) is not None:
                    game_finished = True

                pygame.display.update()
                if game_finished == False and to_move == "O":
                    board, to_move = AI.add_XO_AI(board, graphical_board, to_move, X_IMG, O_IMG, SCREEN, board_size)
                    if game_finished:
                        reset_board()

                    if check_win_2(board) is not None:
                        game_finished = True

                pygame.display.update()
