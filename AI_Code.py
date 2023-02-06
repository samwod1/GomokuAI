import copy
import math as math1
import random
import time as timer

import pygame
import Game_Code
import initialise

board_size = initialise.board_size
winCondition = initialise.winCondition
computerTurn = initialise.computerTurn
maxDepth = 10


def result(state, action):
    s = copy.deepcopy(state)
    x = action[0][0]
    y = action[0][1]
    turn = copy.deepcopy(action[1])

    s[0][y][x] = turn

    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'

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
               # next_state[i][j] = to_move
                actions.append([[j, i], to_move])  # [[x, y], to_move]

    #print("actions!!: " + str(actions))

    return actions


def terminal_test(state):

    global board_size, winCondition
    current_board = (state[0])
    dim = board_size
    dum = dim - (winCondition - 1)

    win_found = False
    winner = None

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
            return True, 0, []

    if winner == 'O':
        return True, 1, []
    elif winner == 'X':
        return True, -1, []

    return False, 2, []

def successors(state):
    s = copy.deepcopy(state)
    to_move = s[1]

    if to_move == 1:
        to_move = 'X'
    else:
        to_move = 'O'

    if to_move == 'X':
        to_move_num = 0
    else:
        to_move_num = 1

    current_board = s[0]
    res = []

    for i in range(board_size):
        for j in range(board_size):
            # print("current board: " + str(current_board))
            next_state = copy.deepcopy(current_board)
            # print("next state: " + str(next_state))
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                next_state[i][j] = to_move
                res.append([next_state, to_move_num])
    #  print(res)

    return res

def rollout(state):
    bestPath = []
    while True:
        # print(state)
        terminal, utility, path = terminal_test(state)
        if terminal:
            return utility
        else:
            succ = successors(state)
            index = random.randint(0, len(succ) - 1)
            state = succ[index]
            bestPath.append(state)



# rollout function
def MCR_player(state):
    s = copy.deepcopy(state)
    turn = s[1]
    print("turn: " + str(turn))
    print("state: " + str(state))
    n = 50  # performs n many rollouts
    # print("n: " + str(n))
    rolloutSim = rollout(s)  # first rollout

    for i in range(n):
        nextRollout = rollout(s)
        print("rolloutSim: " + str(rolloutSim[0]))
        print("nextRollout: " + str(nextRollout[0]))
        print("turn: " + str(turn))
        if rolloutSim[0] < nextRollout[0] and turn == 0:
            print("changing Rollout!! O")
            rolloutSim = nextRollout
        elif rolloutSim[0] > nextRollout[0] and turn == 1:
            print("changing Rollout!! O")
            rolloutSim = nextRollout

    # print("rolloutSim" + str(rolloutSim))

    return rolloutSim

def minValue(state, depth):
    print("  ")
    print("<<<<<<< MIN VALUE >>>>>>>")
    print(" ")
    fin, utility, path = terminal_test(state)

    if depth >= maxDepth:
        return MCR_player(state)
    else:
        depth += 1

    if fin:
        print("returning utlity: " + str(utility) + " on state: " + str(state))
        return utility

    else:

        v = math1.inf
        actions = getActions(state)
        print("looping through actions on state: " + str(state))
        for a in actions:
            r = result(state, a)
            print("got result: " + str(r) + " from action: " + str(a))
            v = min(v, maxValue(r, depth))
        return v


def maxValue(state, depth):
    print("  ")
    print("<<<<<<< MAX VALUE >>>>>>>")
    print(" ")

    if depth >= maxDepth:
        return MCR_player(state)
    else:
        depth += 1

    fin, utility, path = terminal_test(state)
    if fin:
        print("returning utlity: " + str(utility) + " on state: " + str(state))
        return utility
    else:
        v = -1 * math1.inf
        actions = getActions(state)
        print("looping through actions on state: " + str(state))
        for a in actions:
            r = result(state, a)
            print("got result: " + str(r) + " from action: " + str(a))
            v = max(v, minValue(r, depth))
        return v


def minimax(state):
    actions = getActions(state)
    depth = 0

    bestActionUtility = -1 * math1.inf
    bestAction = None

    for a in actions:
        r = result(state, a)
        minimum = minValue(r, depth)
        if minimum > bestActionUtility:
            bestAction = a
            bestActionUtility = minimum

    return bestAction


def AI_Player_minimax(state):
    start = timer.time()
    bestAction = minimax(state)
    end = timer.time()
    duration = end-start
    print("")
    print("AI player moved to state " + str(bestAction))
    print("Time taken: " + str(duration))
    return bestAction


def state_conversion(current_board, to_move):
    if to_move == "X":
        state = [current_board, 'X']
    else:
        state = [current_board, 'O']

    return state


def add_XO_AI(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = state_conversion(cbord, to_move)

    action = AI_Player_minimax(state)
    print(getActions([[[1, 2, 'X'], [4, 'O', 6], ['O', 'X', 'O']], 'O']))
    return action
