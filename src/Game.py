import sys
import MCTS
import MinimaxAlphaBeta
import MinimaxRollout
import SimpleMCTS
from Initialise import *

pygame.init()


def drawGrid(screen, size, board_size, distanceBtwRows):
    x = 100
    y = 100

    pygame.draw.line(screen, (0, 0, 0), (x, 100), (x, size + 100))
    pygame.draw.line(screen, (0, 0, 0), (100, y), (size + 100, y))

    for i in range(board_size):
        x += distanceBtwRows
        y += distanceBtwRows
        pygame.draw.line(screen, (0, 0, 0), (x, 100), (x, size + 100))
        pygame.draw.line(screen, (0, 0, 0), (100, y), (size + 100, y))


# redraws the grid shown on screen and updates the display
def redraw():
    drawGrid(SCREEN, BOARD_SIZE, board_size, distanceBtwRows)
    pygame.display.update()


# resets all relevant game values to restart the game
def resetBoard():
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


def renderBoard(board, X_IMG, O_IMG):
    global graphical_board
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = X_IMG
                graphical_board[i][j][1] = X_IMG.get_rect(center=(j * distanceBtwRows + 121, i * distanceBtwRows + 121))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = O_IMG
                graphical_board[i][j][1] = O_IMG.get_rect(center=(j * distanceBtwRows + 121, i * distanceBtwRows + 121))


def playTurn(board, graphical_board, to_move):
    if to_move == humanTurn and not game_finished:
        action = humanAction()
        if action is not None:
            board, to_move = renderPiece(action, board, graphical_board)

    elif to_move == computerTurn and not game_finished:
        action = computerAction(board)
        board, to_move = renderPiece(action, board, graphical_board)

    return board, to_move


def humanAction():
    current_pos = pygame.mouse.get_pos()
    converted_x = round((current_pos[0] - 97.5) // distanceBtwRows)  # muck about with these values
    converted_y = round((current_pos[1] - 97.5) // distanceBtwRows)

    if (board_size - 1) >= converted_y >= 0 and (board_size - 1) >= converted_x >= 0:
        action = [[converted_x, converted_y], humanTurn]
    else:
        action = None  # incase the human clicks somewhere not allowed

    return action


def computerAction(board):

    if ai_type == 'MCTS':
        action = MCTS.AI_play(board, to_move)
    elif ai_type == 'SimpleMCTS':
        action = SimpleMCTS.AIPlay(board, to_move)
    elif ai_type == 'MinimaxAlphaBeta':
        action = MinimaxAlphaBeta.AIPlay(board, to_move)
    elif ai_type == 'MinimaxRollout':
        action = MinimaxRollout.AIPlay(board, to_move)
    else:
        print("Invalid 'ai_type' selected, Defaulting to MCTS")
        action = MCTS.AI_play(board, to_move)

    return action


def renderPiece(action, board, graphical_board):
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

        renderBoard(board, X_IMG, O_IMG)

        for i in range(board_size):
            for j in range(board_size):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

    return board, to_move


# goes through board array and checks if the game is finished
def checkWin(current_board):
    dim = board_size
    dum = dim - (win_condition - 1)  # index for the number of tiles to check for a win
    win_found = False
    winner = None
    win_type = None
    win_position = (0, 0)

    while not win_found:

        for i in range(dim):
            for j in range(dum):
                winConditionCount = (win_condition - 1)
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
                winConditionCount = (win_condition - 1)
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

        for i in range((win_condition - 1), dim):
            for j in range(dum):
                winConditionCount = (win_condition - 1)
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

        for i in range((win_condition - 1), dim):
            for j in range((win_condition - 1), dim):
                winConditionCount = (win_condition - 1)
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
        return "DRAW"

    if winner is not None:
        winConditionCount = win_condition - 1
        i = win_position[0]
        j = win_position[1]
        if win_type == "horizontal":
            while winConditionCount >= 0:
                graphical_board[i][j + winConditionCount][0] = WINNER_IMG
                SCREEN.blit(graphical_board[i][j + winConditionCount][0],
                            graphical_board[i][j + winConditionCount][1])  #
                winConditionCount -= 1

        winConditionCount = win_condition - 1
        if win_type == "vertical":
            while winConditionCount >= 0:
                graphical_board[i + winConditionCount][j][0] = WINNER_IMG
                SCREEN.blit(graphical_board[i + winConditionCount][j][0], graphical_board[i + winConditionCount][j][1])
                winConditionCount -= 1

        winConditionCount = win_condition - 1
        if win_type == "diagonals":
            while winConditionCount >= 0:
                graphical_board[i - winConditionCount][j + winConditionCount][0] = WINNER_IMG
                SCREEN.blit(graphical_board[i - winConditionCount][j + winConditionCount][0],
                            graphical_board[i - winConditionCount][j + winConditionCount][1])
                winConditionCount -= 1

        winConditionCount = win_condition - 1
        if win_type == "other diagonals":
            while winConditionCount >= 0:
                graphical_board[i - winConditionCount][j - winConditionCount][0] = WINNER_IMG
                SCREEN.blit(graphical_board[i - winConditionCount][j - winConditionCount][0],
                            graphical_board[i - winConditionCount][j - winConditionCount][1])
                winConditionCount -= 1

        pygame.display.update()

    return winner

# game loop for a human playing an AI, much simpler method if its just two computers playing each other

def gameLoop():
    global board, board_size, graphical_board, to_move, game_finished, move_first
    while True:
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if move_first == computerTurn and to_move == computerTurn:
                move_first = None
                board, to_move = playTurn(board, graphical_board, to_move)

                if game_finished:
                    resetBoard()

                if checkWin(board) is not None:
                    game_finished = True

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:  # gets the events from the event queue, checks if its mouse down

                board, to_move = playTurn(board, graphical_board, to_move)

                if game_finished:
                    resetBoard()

                if checkWin(board) is not None:
                    game_finished = True

                pygame.display.update()

                if game_finished is False and to_move == computerTurn:

                    board, to_move = playTurn(board, graphical_board, to_move)

                    if game_finished:
                        resetBoard()

                    if checkWin(board) is not None:
                        game_finished = True

                pygame.display.update()
