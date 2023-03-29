# Functions used by all AI players
import copy
import random
from Initialise import board_size, win_condition, humanTurn, computerTurn


def result(state, action):
    s = copy.deepcopy(state)
    x = action[0][0]
    y = action[0][1]
    turn = copy.deepcopy(action[1])

    if turn == 'X':
        turn = 'O'
        s[0][y][x] = 'X'
    else:
        turn = 'X'
        s[0][y][x] = 'O'

    s[1] = turn
    # print("state: " + str(state))
    return s


def getActions(state):
    to_move = state[1]
    actions = []

    next_state = state[0]

    for i in range(board_size):
        for j in range(board_size):
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                actions.append([[j, i], to_move])  # [[x, y], to_move]

    return actions


def rollout(s):
    state = s[:]
    while True:
        terminal, utility, path = terminalTest(state)
        if terminal:
            return utility
        else:
            succ = successors(state)
            index = random.randint(0, len(succ) - 1)
            state = succ[index][:]


# returns a tuple of a boolean, value and empty state
# boolean: is True if the state passed is terminal, false otherwise.
# value: is 1 if it's a win, -1 for a loss and 0 if draw
def terminalTest(state):
    current_board = state[0]
    dim = len(state[0])
    dum = dim - (win_condition - 1)

    win_found = False
    winner = None

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
                    win_found = True

        break

    if not win_found:
        draw_found = True
        for i in range(dim):
            for j in range(dim):
                if current_board[i][j] != 'X' and current_board[i][j] != 'O':
                    draw_found = False
                    break

        if draw_found:
            # print("DRAW FOUND: " + str(state))
            return True, 0, []

    if winner == humanTurn:
        return True, -1, []
    elif winner == computerTurn:
        return True, 1, []

    return False, None, []


def successors(state):
    to_move = state[1]
    size = len(state[0])
    if to_move == 1:
        to_move = 'X'
    else:
        to_move = 'O'

    if to_move == 'X':
        to_move_num = 0
    else:
        to_move_num = 1

    current_board = state[0]
    res = []

    for i in range(size):
        for j in range(size):
            next_state = [row[:] for row in current_board]
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                next_state[i][j] = to_move
                res.append([next_state, to_move_num])

    return res


def stateToAction(init_state, bestState):
    x_pos = -1
    y_pos = -1
    size = len(init_state[0])
    if bestState[1] == 1:
        turn = 'O'
    else:
        turn = 'X'
    action = None

    for i in range(size):
        y_pos = y_pos + 1
        for j in range(size):
            x_pos = x_pos + 1
            if init_state[i][j] != bestState[0][i][j]:
                action = [[j, i], turn]
                break

    return action


def stateConversion(board, to_move):
    if to_move == 'X':
        return [board, 1]
    else:
        return [board, 0]


def setTimeLimit():
    if board_size == 3:
        return 3
    elif board_size == 4:
        return 4
    elif board_size == 5:
        return 5
    elif board_size == 6:
        return 9
    elif board_size == 7:
        return 15
    elif board_size == 8:
        return 13
    elif board_size == 10:
        return 25
    else:
        return 5

