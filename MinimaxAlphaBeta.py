# Library imports
import copy
import math as math1
import time as timer

# File imports
import Initialise
from AI import *

board_size = Initialise.board_size
winCondition = Initialise.winCondition
computerTurn = Initialise.computerTurn


def getActions(state):
    to_move = state[1]
    actions = []

    next_state = state[0]

    for i in range(board_size):
        for j in range(board_size):
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                # next_state[i][j] = to_move
                actions.append([[j, i], to_move])  # [[x, y], to_move]

    # print("actions!!: " + str(actions))

    return actions


def minValue(state, alpha, beta):
    print("  ")
    print("<<<<<<< MIN VALUE >>>>>>>")
    print(" ")
    fin, utility, path = terminal_test(state)

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
            v = min(v, maxValue(r, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def maxValue(state, alpha, beta):
    print("  ")
    print("<<<<<<< MAX VALUE >>>>>>>")
    print(" ")

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
            v = max(v, minValue(r, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    # rollout function


def minimax(state):
    alpha = -math1.inf
    beta = math1.inf

    actions = getActions(state)

    bestActionUtility = -1 * math1.inf
    bestAction = None

    for a in actions:
        r = result(state, a)
        minimum = minValue(r, alpha, beta)
        if minimum > bestActionUtility:
            bestAction = a
            bestActionUtility = minimum

    return bestAction


def AI_Player_minimax(state):
    start = timer.time()
    bestAction = minimax(state)
    end = timer.time()
    duration = end - start
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
