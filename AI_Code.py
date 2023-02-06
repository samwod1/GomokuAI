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
maxDepth = 3


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
    s = copy.deepcopy(state)
    while True:
        terminal, utility, path = terminal_test(s)
        if terminal:
            return utility
        else:
            succ = successors(s)
            index = random.randint(0, len(succ) - 1)
            s = succ[index]



def MCR_player(state):
    print("state: " + str(state))
    s = copy.deepcopy(state)
    n = 15  # performs n many rollouts
    rolloutValue = 0
    for i in range(n):
        nextRollout = rollout(s)
        if nextRollout == -1:
            print("rollout Black wins")
        elif nextRollout == 1:
            print("rollout White wins")
        elif nextRollout == 0:
            print("rollout draw")
        rolloutValue = rolloutValue + nextRollout

    if rolloutValue == 0:
        rolloutValue = 0
    elif rolloutValue > 0:
        rolloutValue = 1
    elif rolloutValue < 0:
        rolloutValue = -1

    return rolloutValue

def minValue(state, depth, alpha, beta):
    print("  ")
    print("<<<<<<< MIN VALUE >>>>>>>")
    print(" ")
    fin, utility, path = terminal_test(state)

    if depth >= maxDepth:
        print("DEPTH REACHED, ROLLING OUT")
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
            v = min(v, maxValue(r, depth, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def maxValue(state, depth, alpha, beta):
    print("  ")
    print("<<<<<<< MAX VALUE >>>>>>>")
    print(" ")

    if depth >= maxDepth:
        print("DEPTH REACHED, ROLLING OUT")
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
            v = max(v, minValue(r, depth, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v


def minimax(state):
    actions = getActions(state)
    depth = 0
    alpha = 0
    beta = 0

    bestActionUtility = -1 * math1.inf
    bestAction = None

    for a in actions:
        r = result(state, a)
        minimum = minValue(r, depth, alpha, beta)
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
    return action
