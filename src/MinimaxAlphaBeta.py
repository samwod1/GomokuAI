# Library imports
import math as m
import time as timer

# File imports
from AI import terminalTest, getActions, result, copy, stateConversion, stateToAction


def minValue(state, alpha, beta):
    fin, utility, path = terminalTest(state)

    if fin:
        return utility

    else:

        v = m.inf
        actions = getActions(state)
        for a in actions:
            r = result(state, a)
            v = min(v, maxValue(r, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def maxValue(state, alpha, beta):

    fin, utility, path = terminalTest(state)

    if fin:
        return utility
    else:
        v = -1 * m.inf
        actions = getActions(state)
        for a in actions:
            r = result(state, a)
            v = max(v, minValue(r, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


def minimaxAlphaBeta(state):
    alpha = -m.inf
    beta = m.inf

    actions = getActions(state)
    print(actions)
    bestActionUtility = -1 * m.inf
    bestAction = None

    for a in actions:
        r = result(state, a)
        print(r)
        minimum = minValue(r, alpha, beta)
        if minimum > bestActionUtility:
            bestAction = a
            bestActionUtility = minimum

    return bestAction


def MinimaxInit(state):
    start = timer.time()
    bestAction = minimaxAlphaBeta(state)
    end = timer.time()
    duration = end - start
    print("")
    print("AI player moved to state " + str(bestAction))
    print("Time taken: " + str(duration))
    if state[1] == 0:
        return [bestAction[0], 'O']
    else:
        return [bestAction[0], 'X']


def state_conversion(current_board, to_move):
    if to_move == "X":
        state = [current_board, 'X']
    else:
        state = [current_board, 'O']

    return state


def AIPlay(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = stateConversion(cbord, to_move)

    action = MinimaxInit(state)
    return action
