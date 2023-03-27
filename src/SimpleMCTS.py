# Library imports
import math as m
import time as timer

# File imports
from src.AI import *


def MCTS(state):
    s = copy.deepcopy(state)
    bestNextState = expand(s)
    return bestNextState


def MCR(state):
    s = state[:]
    n = 1000  # performs n many rollouts
    rolloutValue = 0

    for i in range(n):
        rolloutValue = rolloutValue + (rollout(s))

    return rolloutValue


def expand(node):
    # gets all the successors of the node and rollouts out through them all
    current = node[:]
    succ = successors(current)
    bestState = None
    maxValue = -m.inf
    for s in succ:
        rolloutValue = MCR(s)
        if rolloutValue > maxValue:
            maxValue = rolloutValue
            bestState = s[:]

    return bestState


def MCTSInit(state):
    start = timer.time()
    game_state = MCTS(state)
    end = timer.time()
    duration = end - start
    print("")
    print("AI player moved to state " + str(game_state))
    print("Time taken: " + str(duration))
    return game_state


def AIPlay(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = stateConversion(cbord, to_move)

    state = MCTSInit(state)

    action = stateToAction(cbord, state)
    if action is not None:
        return action
    else:
        return [[]]
