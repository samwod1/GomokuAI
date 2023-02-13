#returns the best possible action to do with that board
import copy
import random

import time
import initialise
import math as math1

tree = {}
og_state = copy.deepcopy(initialise.board)
board_size = initialise.board_size
winCondition = initialise.winCondition

def add_XO_AI(board, to_move):
    cbord = copy.deepcopy(board)
    state = state_conversion(cbord, to_move)
    print("AI operating on state: " + str(state))
    state = MCTSPlayer(state)
    action = stateToAction(cbord, state)
    print("returning action: " + str(action))

    if action is not None:
        return action
    else:
        return [[]]

def state_conversion(board, to_move):
    if to_move == 'X':
        return [board, 1]
    else:
        return [board, 0]


def MCTSPlayer(state):
    print("Starting MCTS")
    start = time.time()
    action = MCTS(state)
    end = time.time()
    duration = end-start
    print("")
    print("AI player moved to state: " + str(action))
    print("In time: " + str(duration))

    return action


def MCTS(state):
    global tree
    tree.clear()
    tree["[]"] = ["start", '0', '0']
    tree[str(state)] = ["[]", '0', '0'] #initial tree node (parent, value, visits)

    iterations = 0
    while iterations < 75:
        traverse_and_expand(copy.deepcopy(state))
        iterations += 1

    succ = successors(copy.deepcopy(state))
    print("Tree: " + str(tree))
    maxUCB = -math1.inf
    bestNextState = succ[0]
    for s in succ:
        print("successor: " + str(s))
        thisUCB = calcMaxUCB(s)
        print("UCB: " + str(thisUCB))
        if thisUCB > maxUCB:
            print("UCB is better than: " + str(maxUCB))
            print("Replacing: " + str(bestNextState) + " with " + str(s))
            maxUCB = thisUCB
            bestNextState = copy.deepcopy(s)
    return bestNextState


def traverse_and_expand(state):
    global tree
    current = copy.deepcopy(state)
    maxUCB = -math1.inf
    minUCB = math1.inf
    UCBNode = current

    while not isLeaf(current):
        #print(str(current) + " is not a leaf!")
        succ = successors(copy.deepcopy(current))
        print("adding successors to tree" + str(succ))
        for s in succ:
            print("s: " + str(s))
            #add successors to the tree
            if tree.get(str(s)) is None: #check to see if the successor is already in the tree, so it doesnt overwrite its stats
                tree[str(s)] = [str(current), '0', '0']
            else:
                print("successor already in tree")

            # UCB = calcMaxUCB(s)
            # if UCB > maxUCB:
            #     maxUCB = UCB
            #     UCBNode = copy.deepcopy(s)

            # calcuate ucb for successor
            if s[1] == 0:
                print("calculating max UCB")
                UCB = calcMaxUCB(s)
                if UCB > maxUCB:
                    maxUCB = UCB
                    UCBNode = copy.deepcopy(s)
            elif s[1] == 1:
                print("calculating min UCB")
                UCB = calcMinUCB(s)
                if UCB < minUCB:
                    minUCB = UCB
                    UCBNode = copy.deepcopy(s)

        print("moving down the tree, current: " + str(current) + " is now " + str(UCBNode))
        current = copy.deepcopy(UCBNode)

    if tree[str(current)][2] == 0:
        print("tree1: " + str(tree))
        print(str(current) + " is  a leaf! and hasnt been visited")
        value = MCR_player(copy.deepcopy(current))
        print("TRAVERSE AND EXPAND CURRENT: " + str(current))
        backpropagate(copy.deepcopy(current), value)
    else:
        print("tree2: " + str(tree))
        print(str(current) + " is  a leaf! and has been visited")
        succ = successors(current)
        print("adding successors to tree: " + str(succ))
        for s in succ:
            print("s: " + str(s))
            if tree.get(str(s)) is None:
                tree[str(s)] = [str(current), '0', '0']  # adding successors to tree
            else:
                print("successor already in tree")

        current = copy.deepcopy(succ[0])  # current = first new child node
        value = MCR_player(current)  # rollout value
        print("TRAVERSE AND EXPAND CURRENT: " + str(current))
        backpropagate(copy.deepcopy(current), value)


def MCR_player(state):
    print("state: " + str(state))
    s = copy.deepcopy(state)
    n = 50  # performs n many rollouts
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

    #maybe get rid of this check
    if rolloutValue <= 0:
        rolloutValue = -1
    elif rolloutValue > 0:
        rolloutValue = 1
    print("Monte Carlo has returned: " + str(rolloutValue))
    return rolloutValue


def backpropagate(node, rolloutValue):
    global tree
    print("BACK PROPOGATION NODE: " + str(node))

    current = copy.deepcopy(node)
    print("BACK PROPOGATION CURRENT: " + str(current))
    while tree[str(current)][0] != "start":
        tree[str(current)] = [str(tree[str(current)][0]), str(int(tree[str(current)][1]) + rolloutValue), str(int(tree[str(current)][2]) + 1)]
        print("Backpropogating: " + str([tree[str(current)]]))
        current = copy.deepcopy(tree[str(current)][0])  # current becomes parent node
        print("back propogate current: " + str(current))


def rollout(s):
    state = copy.deepcopy(s)
    print("ROLLOUT COMMENCING")
    print("from: " + str(state))
    while True:
        terminal, utility, path = terminal_test(state)
        if terminal:
            print("terminal, utility: " + str(utility))
            print("state: " + str(state))
            return utility
        else:
            succ = successors(state)
            index = random.randint(0, len(succ) - 1)
            state = copy.deepcopy(succ[index])


def isLeaf(state):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    for i in range(len(treeValues)):
        if treeValues[i][0] == state:
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    if leafBool:
        print("Tree: " + str(tree))
        print(str(state) + " is a leaf!")
    else:
        print("Tree: " + str(tree))
        print(str(state) + " is not a leaf!")
    return leafBool


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


def successors(state):
    to_move = state[1]

    if to_move == 1:
        to_move = 'X'
    else:
        to_move = 'O'

    if to_move == 'X':
        to_move_num = 0
    else:
        to_move_num = 1

    current_board = state[0]
    res = []

    for i in range(board_size):
        for j in range(board_size):
            next_state = copy.deepcopy(current_board)
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                next_state[i][j] = to_move
                res.append([next_state, to_move_num])

    return res


def calcMinUCB(state):
    C = 2
    # if empty node make it inf else apply UCB1 formula
    if tree[str(state)][1] == '0' and tree[str(state)][2] == '0':
        UCB = -math1.inf
    else:
        # apply UCB, made first parameter negative
        UCB = int(tree[str(state)][1]) - C * math1.sqrt((math1.log(int(tree[str(tree[str(state)][0])][2]) / int(tree[str(state)][2]))))
    #print("calcMinUCB: " + str(UCB))
    return UCB

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


def calcMaxUCB(state):
    C = 2
    # if empty node make it inf else apply UCB1 formula
    if tree[str(state)][1] == '0' and tree[str(state)][2] == '0':
        UCB = math1.inf
    else:
        # apply UCB, made first parameter negative
        UCB = int(tree[str(state)][1]) + C * math1.sqrt((math1.log(int(tree[str(tree[str(state)][0])][2]) / int(tree[str(state)][2]))))
    print("FuncCalcMaxUCB: " + str(UCB))
    return UCB









