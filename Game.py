import sys
import time

import pygame
import MCTS
import Minimax
import initialise
from initialise import *
import CSV_Writer

pygame.init()

maxGames = 30

gamesPlayed = 0
minimaxWins = 0
mctsWins = 0
draws = 0


def get_board_size():
    return board_size


def grid(SCREEN, size, board_size, distanceBtwRows):
    x = 100
    y = 100

    pygame.draw.line(SCREEN, (0, 0, 0), (x, 100), (x, size + 100))
    pygame.draw.line(SCREEN, (0, 0, 0), (100, y), (size + 100, y))

    for i in range(board_size):
        x += distanceBtwRows
        y += distanceBtwRows
        pygame.draw.line(SCREEN, (0, 0, 0), (x, 100), (x, size + 100))
        pygame.draw.line(SCREEN, (0, 0, 0), (100, y), (size + 100, y))


def redraw():
    global SCREEN, WIDTH, board_size, distanceBtwRows

    grid(SCREEN, BOARD_SIZE, board_size, distanceBtwRows)
    pygame.display.update()


def reset_board():
    global graphical_board, board, to_move, game_finished, move_first

    board = []
    count = 0

    for i in range(board_size):
        count += 1
        board.append([count])
        for j in range(board_size - 1):
            count += 1
            board[i].append(count)

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
                graphical_board[i][j][1] = X_IMG.get_rect(center=(j * distanceBtwRows + 121, i * distanceBtwRows + 121))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = O_IMG
                graphical_board[i][j][1] = O_IMG.get_rect(center=(j * distanceBtwRows + 121, i * distanceBtwRows + 121))


def add_XO(board, graphical_board, to_move):
    if to_move == minimaxTurn and not game_finished:
        action = minimaxAction()
        board, to_move = addPiece(action, board, graphical_board)

    elif to_move == mctsTurn and not game_finished:
        action = mctsAction(board)
        board, to_move = addPiece(action, board, graphical_board)

    return board, to_move


def humanAction():
    current_pos = pygame.mouse.get_pos()
    converted_x = round((current_pos[0] - 97.5) // distanceBtwRows)  # muck about with these values
    converted_y = round((current_pos[1] - 97.5) // distanceBtwRows)

    if (board_size - 1) >= converted_y >= 0 and (board_size - 1) >= converted_x >= 0:
        action = [[converted_x, converted_y], minimaxTurn]
    else:
        action = None  # incase the human clicks somewhere not allowed

    return action


def minimaxAction():
    action = Minimax.add_XO_AI(board, to_move)
    return action


def mctsAction(board):
    action = MCTS.add_XO_AI(board, to_move)
    return action


def addPiece(action, board, graphical_board):
    x = action[0][0]
    y = action[0][1]
    turn = action[1]
    to_move = turn

    if board[y][x] != 'O' and board[y][x] != 'X':
        board[y][x] = turn
        if turn == "X":
            to_move = "O"
        else:
            to_move = "X"

        render_board(board, X_IMG, O_IMG)

        for i in range(board_size):
            for j in range(board_size):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

    return board, to_move


def check_win(current_board):
    global minimaxWins, mctsWins, draws
    dim = board_size
    dum = dim - (winCondition - 1)
    win_found = False
    winner = None
    win_type = None
    win_position = (0, 0)

    while not win_found:

        for i in range(dim):
            for j in range(dum):
                winConditionCount = (winCondition - 1)
                sequenceBroken = False
                while not sequenceBroken and winConditionCount >= 0:
                    if current_board[i][j] == current_board[i][j + winConditionCount]:
                        winConditionCount -= 1
                    else:
                        sequenceBroken = True
                if not sequenceBroken:
                    winner = current_board[i][j]
                    win_position = (i, j)
                    win_type = "horizontal"
                    win_found = True

        for i in range(dum):
            for j in range(dim):
                winConditionCount = (winCondition - 1)
                sequenceBroken = False
                while not sequenceBroken and winConditionCount >= 0:
                    if current_board[i][j] == current_board[i + winConditionCount][j]:
                        winConditionCount -= 1
                    else:
                        sequenceBroken = True
                if not sequenceBroken:
                    winner = current_board[i][j]
                    win_position = (i, j)
                    win_type = "vertical"
                    win_found = True

        for i in range((winCondition - 1), dim):
            for j in range(dum):
                winConditionCount = (winCondition - 1)
                sequenceBroken = False
                while not sequenceBroken and winConditionCount >= 0:
                    if current_board[i][j] == current_board[i - winConditionCount][j + winConditionCount]:
                        winConditionCount -= 1
                    else:
                        sequenceBroken = True

                if not sequenceBroken:
                    winner = current_board[i][j]
                    win_position = (i, j)
                    win_type = "diagonals"
                    win_found = True

        for i in range((winCondition - 1), dim):
            for j in range((winCondition - 1), dim):
                winConditionCount = (winCondition - 1)
                sequenceBroken = False
                while not sequenceBroken and winConditionCount >= 0:
                    if current_board[i][j] == current_board[i - winConditionCount][j - winConditionCount]:
                        winConditionCount -= 1
                    else:
                        sequenceBroken = True

                if not sequenceBroken:
                    winner = current_board[i][j]
                    win_position = (i, j)
                    win_type = "other diagonals"
                    win_found = True

        break

    if not win_found:
        for i in range(dim):
            for j in range(dim):
                if current_board[i][j] != 'X' and current_board[i][j] != 'O':
                    return None
        draws += 1
        return "DRAW"

    if winner == 'X':
        winner_IMG = X_WIN
    else:
        winner_IMG = O_WIN

    if winner is not None:
        winConditionCount = winCondition - 1
        i = win_position[0]
        j = win_position[1]
        if win_type == "horizontal":
            while winConditionCount >= 0:
                graphical_board[i][j + winConditionCount][0] = winner_IMG
                SCREEN.blit(graphical_board[i][j + winConditionCount][0],
                            graphical_board[i][j + winConditionCount][1])  #
                winConditionCount -= 1

        winConditionCount = winCondition - 1
        if win_type == "vertical":
            while winConditionCount >= 0:
                graphical_board[i + winConditionCount][j][0] = winner_IMG
                SCREEN.blit(graphical_board[i + winConditionCount][j][0], graphical_board[i + winConditionCount][j][1])
                winConditionCount -= 1

        winConditionCount = winCondition - 1
        if win_type == "diagonals":
            while winConditionCount >= 0:
                graphical_board[i - winConditionCount][j + winConditionCount][0] = winner_IMG
                SCREEN.blit(graphical_board[i - winConditionCount][j + winConditionCount][0],
                            graphical_board[i - winConditionCount][j + winConditionCount][1])
                winConditionCount -= 1

        winConditionCount = winCondition - 1
        if win_type == "other diagonals":
            while winConditionCount >= 0:
                graphical_board[i - winConditionCount][j - winConditionCount][0] = winner_IMG
                SCREEN.blit(graphical_board[i - winConditionCount][j - winConditionCount][0],
                            graphical_board[i - winConditionCount][j - winConditionCount][1])
                winConditionCount -= 1

        pygame.display.update()

    if winner == minimaxTurn:
        minimaxWins += 1
    elif winner == mctsTurn:
        mctsWins += 1

    return winner

def reset_stats():
    global gamesPlayed, minimaxWins, mctsWins, draws

    gamesPlayed = 0
    minimaxWins = 0
    mctsWins = 0
    draws = 0


def game_loop():
    global board, board_size, graphical_board, to_move, game_finished, move_first, gamesPlayed, maxGames
    while MCTS.getTotalIterations() <= 1000:
        while gamesPlayed < maxGames:
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            board, to_move = add_XO(board, graphical_board, to_move)

            if game_finished:
                reset_board()

            if check_win(board) is not None:
                gamesPlayed += 1
                game_finished = True

            pygame.display.update()

        # CSV_Writer.appendC(MCTS.getC())
        # CSV_Writer.appendLosses(minimaxWins)

        CSV_Writer.appendIterations(MCTS.getTotalIterations())
        CSV_Writer.appendLosses(minimaxWins)

        print("Losses: " + str(minimaxWins))
        print("C: " + str(MCTS.getC()))

        #MCTS.incrementC(0.1)

        MCTS.incrementTotalIterations(100)
        reset_stats()

    #Write to CSV
    #CSV_Writer.CSV_C_Losses()
    CSV_Writer.CSV_Iterations_Losses()
    print("GAMES FINISHED \n Minimax Wins: " + str(minimaxWins) + " \n MCTS Wins: " + str(mctsWins) + " \n Draws: " + str(draws))
