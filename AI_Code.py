import copy
import math as math1
import random
import time as timer

import pygame
import Game_Code
import initialise

board_size = initialise.board_size
init_board = initialise.board
winCondition = initialise.winCondition


def MCTS(state):
    print("FIRST STATE: " + str(state))
    s = copy.deepcopy(state)
    bestNextState = traverse_and_expand(s)
    return bestNextState


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


def terminal_test(state):
    global board_size, winCondition
    current_board = state[0]
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

    if winner == 'X':
        return True, -1, []
    elif winner == 'O':
        return True, 1, []

    return False, 2, []


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


# rollout function
def MCR_player(state):
    print("state: " + str(state))
    s = copy.deepcopy(state)
    turn = s[1]
    n = 100  # performs n many rollouts
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

    # for i in range(n):
    #     nextRollout = rollout(s)
    #     print("nextRollout: " + str(nextRollout))
    #     print("rolloutSim: " + str(rolloutSim))
    #     if rolloutSim < nextRollout and turn == 0:
    #         print("switching, rolloutSim: " + str(rolloutSim) + " nextRollout: " + str(nextRollout) + " on turn: " + str(turn))
    #         rolloutSim = nextRollout
    #     elif rolloutSim > nextRollout and turn == 1:
    #         print("switching, rolloutSim: " + str(rolloutSim) + " nextRollout: " + str(nextRollout) + " on turn: " + str(turn))
    #         rolloutSim = nextRollout
    #     else:
    #         print("no switching")

    return rolloutValue

def traverse_and_expand(node):
    #gets all the successors of the node and rollouts out through them all
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
