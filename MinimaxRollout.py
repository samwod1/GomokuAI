import math as m
import time as timer

from AI import *

maxDepth = 2


def MCR_player(state):
    return rollout(state)


def minValue(state, depth, alpha, beta):
    print("  ")
    print("<<<<<<< MIN VALUE >>>>>>>")
    print(" ")
    fin, utility, path = terminal_test(state)

    if depth >= maxDepth:
        return MCR_player(state)

    if fin:
        print("returning utlity: " + str(utility) + " on state: " + str(state))
        return utility

    else:

        v = m.inf
        actions = getActions(state)
        print("looping through actions on state: " + str(state))
        for a in actions:
            r = result(state, a)
            print("got result: " + str(r) + " from action: " + str(a))
            v = min(v, maxValue(r, depth + 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def maxValue(state, depth, alpha, beta):
    print("  ")
    print("<<<<<<< MAX VALUE >>>>>>>")
    print(" ")

    if depth >= maxDepth:
        return MCR_player(state)

    fin, utility, path = terminal_test(state)
    if fin:
        print("returning utlity: " + str(utility) + " on state: " + str(state))
        return utility
    else:
        v = -m.inf
        actions = getActions(state)
        print("looping through actions on state: " + str(state))
        for a in actions:
            r = result(state, a)
            print("got result: " + str(r) + " from action: " + str(a))
            v = max(v, minValue(r, depth + 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v


def minimaxRollout(state):
    actions = getActions(state)
    depth = 0
    alpha = -m.inf
    beta = m.inf

    bestActionUtility = -m.inf
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
    bestAction = minimaxRollout(state)
    end = timer.time()
    duration = end - start
    print("")
    print("AI player moved to state " + str(bestAction))
    print("Time taken: " + str(duration))
    return bestAction


def add_XO_AI(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = state_conversion(cbord, to_move)

    action = AI_Player_minimax(state)
    return action
