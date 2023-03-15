# Library imports
import copy
import math as math1
import time as timer

# File imports
import Initialise
from AI import *

board_size = Initialise.board_size
init_board = Initialise.board
winCondition = Initialise.winCondition


def MCTS(state):
    print("FIRST STATE: " + str(state))
    s = copy.deepcopy(state)
    bestNextState = traverse_and_expand(s)
    return bestNextState


def MCR_player(state):
    print("state: " + str(state))
    s = copy.deepcopy(state)
    turn = s[1]
    n = 10  # performs n many rollouts
    rolloutSim = rollout(s)  # first rollout
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

    return rolloutValue


def traverse_and_expand(node):
    # gets all the successors of the node and rollouts out through them all
    current = copy.deepcopy(node)
    succ = successors(current)
    bestState = None
    maxValue = -math1.inf
    for s in succ:
        rolloutValue = MCR_player(s)
        if rolloutValue > maxValue:
            maxValue = rolloutValue
            bestState = copy.deepcopy(s)

    return bestState


def AI_Player_mcts(state):
    start = timer.time()
    game_state = MCTS(state)
    end = timer.time()
    duration = end - start
    print("")
    print("AI player moved to state " + str(game_state))
    print("Time taken: " + str(duration))
    return game_state


def state_conversion(current_board, to_move):
    print(to_move)
    if to_move == "X" or to_move == 1:
        state = [current_board, 1]
    else:
        state = [current_board, 0]

    return state


def stateToAction(init_state, bestState):
    x_pos = -1
    y_pos = -1
    if bestState[1] == 1:
        turn = 'O'
    else:
        turn = 'X'
    action = None

    for i in range(board_size):
        y_pos = y_pos + 1
        for j in range(board_size):
            x_pos = x_pos + 1
            if init_state[i][j] != bestState[0][i][j]:
                action = [[j, i], turn]
                break

    return action


def add_XO_AI(current_board, to_move):
    cbord = copy.deepcopy(current_board)
    state = state_conversion(cbord, to_move)

    state = AI_Player_mcts(state)

    action = stateToAction(cbord, state)
    if action is not None:
        return action
    else:
        return [[]]
