import copy
import math as math1
import random
import time as timer

import pygame
import Game_Code
import initialise

tree = {}
board_size = initialise.board_size
init_board = initialise.board
winCondition = initialise.winCondition


def MCTS(state):
    global tree
    #tree.clear()
    og_state = [init_board, state[1]]

    # store intitial state, storing total number of nodes and times visited
    tree[str(og_state)] = ['start', 0, 0]  # dict to store node info: parent, t, n

    # add first node
    tree[str(state)] = [og_state, 0, 0]

    # set a timeout
    depth = 3
    iterations = 0
    # Run MCTS
    while iterations < 1000:
        traverse_and_expand(state, depth)
        iterations += 1


    # checks if the tree is empty
    print("tree: " + str(tree))
    # At end of loop identify successors
    succ = successors(state)

    # Apply UCB formula to all successors
    maxValue = -math1.inf
    bestNextState = succ[0]
    for s in succ:
        thisValue = tree[str(s)][1]
        if thisValue > maxValue:
            maxValue = thisValue
            bestNextState = s
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
    bestPath = []
    while True:
        # print(state)
        terminal, utility, path = terminal_test(state)
        if terminal:
            return utility, bestPath
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
    n = 10  # performs n many rollouts
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
        # elif rolloutSim[0] > nextRollout[0] and turn == 1:
        #     print("changing Rollout!! O")
        #     rolloutSim = nextRollout

    # print("rolloutSim" + str(rolloutSim))

    if len(rolloutSim[1]) == 0:
        return rolloutSim[0], [state]
    else:
        return rolloutSim[0], rolloutSim[1][0]


def backpropagate(node, rolloutValue):
    global tree
    current = node
    while tree[str(current)][0] != "start":
        tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue),
                              int(tree[str(current)][2]) + 1]
        print("Backpropogating: " + str([tree[str(current)]]))
        current = tree[str(current)][0]  # current becomes parent node


def isLeaf(node):
    # check if there is a successor state
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    #  print("treeValues: " + str(treeValues))
    for i in range(len(treeValues)):
        if treeValues[i][0] == node:
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    return leafBool


def traverse_and_expand(node, maxDepth):
    # Function to travel the tree and expand it
    global tree
    current = copy.deepcopy(node)
    leastVisits = math1.inf
    depth = 0
    # while current node isn't a leaf node
    while depth <= maxDepth:
        # Generate successors
        succ = successors(copy.deepcopy(current))
        for s in succ:

            if tree.get(str(s)) is None:
                tree[str(s)] = [str(current), 0, 0]

            if tree[str(s)][2] < leastVisits:
                leastVisits = tree[str(s)][2]
                bestNode = copy.deepcopy(s)

        depth = depth + 1
        current = copy.deepcopy(bestNode)

    # rollout from current
    value = MCR_player(copy.deepcopy(current))[0]
    backpropagate(copy.deepcopy(current), value)

    return


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
