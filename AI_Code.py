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
blackWins = 0
whiteWins = 0

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
    tree["[]"] = ["start", 0, 0]
    tree[str(state)] = ["[]", 0, 0] #initial tree node (parent, value, visits)
    print(state)

    iterations = 0
    while iterations < 150:
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

    #s = [[['O', 'X', 'O'], ['X', 'O', 'X'], ['X', 'O', 'X']], 1]
    # value = MCR_player(s)
    # print("White wins: " + str(whiteWins))
    # print("Black wins: " + str(blackWins))
    # print("value:  " + str(value))

    #terminal_test(s)

    return bestNextState


def traverse_and_expand(state):
    global tree
    # print("Tree: " + str(tree))
    # print("traversing and expanding on state: " + str(state))
    current = copy.deepcopy(state)
    UCBNode = copy.deepcopy(current)

    while True:
        maxUCB = -math1.inf
        minUCB = math1.inf
        if isLeaf(current):
            break

        succ = successors(copy.deepcopy(current))
        # print(" successors: " + str(succ))
        for s in succ:
            UCB = calcMaxUCB(s)
            print("max UCB calculated as: " + str(UCB))
            if UCB > maxUCB:
                # print("UCB is bigger than maxUCB: " + str(maxUCB))
                maxUCB = UCB
                UCBNode = copy.deepcopy(s)

            # if s[1] == 0:
            #     print("1 turn s: " + str(s))
            #     UCB = calcMaxUCB(s)
            #     print("max UCB calculated as: " + str(UCB))
            #     if UCB > maxUCB:
            #         print("UCB is bigger than maxUCB: " + str(maxUCB))
            #         maxUCB = UCB
            #         UCBNode = copy.deepcopy(s)
            #         print("UCB node now: " + str(UCBNode))
            # elif s[1] == 1:
            #     print("0 turn s: " + str(s))
            #     UCB = calcMinUCB(s)
            #     print("min UCB calculated as: " + str(UCB))
            #     if UCB < minUCB:
            #         print("UCB is smaller than minUCB: " + str(minUCB))
            #         minUCB = UCB
            #         UCBNode = copy.deepcopy(s)
            #         print("UCB node now: " + str(UCBNode))

        print("Current has been changed from: " + str(current) + " to: " + str(UCBNode))
        current = copy.deepcopy(UCBNode)

    if tree[str(current)][2] == 0:
        print("Current is now a leaf node and hasn't been visited.")
        value = MCR_player(copy.deepcopy(current))
        backpropagate(copy.deepcopy(current), value)

    elif tree[str(current)][2] > 0:
        print("Current is now a leaf node and has been visited.")
        print("Adding successors to tree")
        succ = successors(current)
        if len(succ) != 0:
            for s in succ:
                # print("s: " + str(s))
                if tree.get(str(s)) is None:
                    tree[str(s)] = [str(current), 0, 0]  # adding successors to tree

            print("First new child node is now rolled out on")
            current = succ[0]  # current = first new child node
            value = MCR_player(copy.deepcopy(current))  # rollout value
            backpropagate(current, value)


# def MCR_player(state):
#     global blackWins, whiteWins
#     # print("state: " + str(state))
#     s = copy.deepcopy(state)
#     n = 100  # performs n many rollouts
#     rolloutValue = 0
#     for i in range(n):
#         nextRollout = rollout(s)
#         if nextRollout == -1:
#             blackWins += 1
#             #print("rollout Black wins")
#         elif nextRollout == 1:
#             whiteWins += 1
#            # print("rollout White wins")
#         rolloutValue = rolloutValue + nextRollout
#
#     #maybe get rid of this check
#     if rolloutValue < 0:
#         rolloutValue = -1
#     elif rolloutValue > 0:
#         rolloutValue = 1
#
#     print("Monte Carlo has returned: " + str(rolloutValue))
#     return rolloutValue

def MCR_player(state):
    s = copy.deepcopy(state)
    n = 100
    turn = state[1]
    rolloutValue = rollout(s) #initial rollout
    for i in range(n):
        nextRollout = rollout(s)
        if nextRollout > rolloutValue:
            print("Turn 0 and next rollout: " + str(nextRollout) + " rolloutValue: " + str(rolloutValue))
            rolloutValue = nextRollout

    print("Monte Carlo has returned: " + str(rolloutValue))
    return rolloutValue


def backpropagate(node, rolloutValue):
    global tree
    c = copy.deepcopy(node)
    #print("BACK PROPOGATION CURRENT: " + str(c))
    while tree[str(c)][0] != "start":
        tree[str(c)] = [str(tree[str(c)][0]), tree[str(c)][1] + rolloutValue, int(tree[str(c)][2]) + 1]
       # print("Backpropogating: " + str([tree[str(c)]]))
        c = copy.deepcopy(tree[str(c)][0])  # current becomes parent node
      #  print("back propogate current: " + str(c))


def rollout(s):
    state = copy.deepcopy(s)
    # print("ROLLOUT COMMENCING")
    # print("from: " + str(state))
    while True:
        terminal, utility, path = terminal_test(state)
        if terminal:
            # print("terminal, utility: " + str(utility))
            # print("state: " + str(state))
            return utility
        else:
            succ = successors(state)
           # print("rollout successors: " + str(succ))
            index = random.randint(0, len(succ) - 1)
           # print("picking: " + str(succ[index]))
            state = copy.deepcopy(succ[index])


def isLeaf(state):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    for i in range(len(treeValues)):
        # print("tVal: " + treeValues[i][0])
        # print("str(state): " + str(state))
        if treeValues[i][0] == str(state):
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    # if leafBool:
    #     print("Tree: " + str(tree))
    #     print(str(state) + " is a leaf!")
    # else:
    #     print("Tree: " + str(tree))
    #     print(str(state) + " is not a leaf!")
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
            print("DRAW FOUND: " + str(state))
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
    if tree[str(state)][1] == 0 and tree[str(state)][2] == 0:
        UCB = -math1.inf
    else:
        # apply UCB, made first parameter negative
        UCB = int(tree[str(state)][1]) - C * math1.sqrt((math1.log(tree[str(tree[str(state)][0])][2]) / tree[str(state)][2]))
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
    # print("v: " + str(tree[str(state)][1]))
    # print("C: " + str(C))
    # print("N: " + str(tree[str(tree[str(state)][0])][2]))
    # print("n: " + str(tree[str(state)][2]))

    # if empty node make it inf else apply UCB1 formula
    if tree[str(state)][1] == 0 and tree[str(state)][2] == 0:
        UCB = math1.inf
    else:
        # apply UCB, made first parameter negative
        UCB = int(tree[str(state)][1]) + C * math1.sqrt((math1.log(tree[str(tree[str(state)][0])][2]) / tree[str(state)][2]))
    return UCB









