import math as m
import time as timer

from AI import *

maxDepth = 3


def MCR(state):
    return rollout(state)


def minValue(state, depth, alpha, beta):
    fin, utility, path = terminalTest(state)

    if depth >= maxDepth:
        return MCR(state)

    if fin:
        return utility

    else:

        v = m.inf
        actions = getActions(state)
        for a in actions:
            r = result(state, a)
            v = min(v, maxValue(r, depth + 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def maxValue(state, depth, alpha, beta):

    if depth >= maxDepth:
        return MCR(state)

    fin, utility, path = terminalTest(state)
    if fin:
        return utility
    else:
        v = -m.inf
        actions = getActions(state)
        for a in actions:
            r = result(state, a)
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


def MinimaxInit(state):
    start = timer.time()
    bestAction = minimaxRollout(state)
    end = timer.time()
    duration = end - start
    print("")
    print("AI player moved to state " + str(bestAction))
    print("Time taken: " + str(duration))
    return bestAction


def AIPlay(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = stateConversion(cbord, to_move)

    action = MinimaxInit(state)
    return action
