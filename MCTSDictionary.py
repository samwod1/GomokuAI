# returns the best possible action to do with that board
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
draws = 0
C = 0
total_iterations = 0
time_limit = 5



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
    print("Starting MCTS\n")
    action = MCTS(state)
    print("")
    print("AI player moved to state: " + str(action))

    return action



def MCTS(state):
    global C, tree, blackWins, whiteWins, draws
    blackWins = 0
    whiteWins = 0
    draws = 0

    tree.clear()
    tree["('[]', 'start')"] = ['start', 0, 0]
    tree[str((state, '[]'))] = [('[]', 'start'), 0, 0]
    iterations = 0
    C = math1.sqrt(2)
    current = (state, '[]')
    start = time.time()
    while time.time() < start + time_limit:
        traverse_and_expand(current)
        # printTree()

    maxUCB = -math1.inf

    succ = successors(state)
    C = 0
    for s in succ:
        UCB = calcMaxUCB((s, current[0]))
        if UCB > maxUCB:        # input("press enter")

            maxUCB = UCB
            UCBNode = copy.deepcopy(s)

    # print("Black Wins: " + str(blackWins))
    # print("White Wins: " + str(whiteWins))
    # print("Draws: " + str(draws))

    return UCBNode


def traverse_and_expand(node):
    global tree
    current = copy.deepcopy(node)
    terminalBool = False
    while True:
        node = current[0]
        parent = current[1]
        boolean, value, path = terminal_test(node)
        if boolean:
            terminalBool = True
            break  # stops if the current node is terminal

        #print("Current  " + str(tree.get(str(current))))
        if isLeaf(current):
            break

        maxUCB = -math1.inf

        succ = successors(node)

        for s in succ:
            UCB = calcMaxUCB((s, node))
            if UCB == math1.inf:
                UCBNode = s
                break
            if UCB > maxUCB:
                maxUCB = UCB
                UCBNode = s

        current = (copy.deepcopy(UCBNode), node)

    if not terminalBool:  # checks if the traversal stopped because a terminal leaf
        if tree[str(current)][2] == 0:
            # print("Leaf has no visits \n")
            value = MCR_player(node)
            backpropagate(current, value)
        else:
            # print("Leaf has been visited\n")
            succ = successors(node)
            # print("Rolling out on first child: " + str(succ[0]))
            for s in succ:
                if tree.get(str((s, node))) is None:
                    tree[str((s, node))] = [current, 0, 0]
            firstChild = succ[0]
            value = MCR_player(firstChild)
            backpropagate((firstChild, node), value)
    else:
        # print("Leaf node is terminal: " + str(current))
        # print("No rollout needed, backpropagating utility \n")
        boolean, value, path = terminal_test(node)
        backpropagate(current, value)


def MCR_player(state):
    return rollout(state)


def backpropagate(node, rolloutValue):
    global tree
    current = copy.deepcopy(node)
    # print("backpropagating")
    while tree[str(current)][0] != "start":
        if current[0][1] == 0:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue * -1),
                                  int(tree[str(current)][2]) + 1]
        else:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue),
                                  int(tree[str(current)][2]) + 1]

        current = copy.deepcopy(tree[str(current)][0])


def rollout(s):
    global draws, blackWins, whiteWins
    state = copy.deepcopy(s)
    # print("ROLLOUT COMMENCING FROM: " + str(state))
    while True:
        terminal, utility, path = terminal_test(state)
        if terminal:
            # print("ROLLOUT FINISHED AT STATE: " + str(state))
            # print("WITH UTILITY:" + str(utility) + "\n")
            if utility == 0:
                draws += 1
            elif utility == 1:
                whiteWins += 1
            elif utility == -1:
                blackWins += 1

            return utility
        else:
            succ = successors(state)
            index = random.randint(0, len(succ) - 1)
            state = copy.deepcopy(succ[index])


def isLeaf(node):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    for i in range(len(treeValues)):
        if treeValues[i][0] == node:
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    return leafBool  # if leafBool:


def calcMaxUCB(current):
    global tree
    node = tree.get(str(current))
    parentNodeVisits = tree[str(node[0])][2]
    visits = node[2]
    value = node[1]

    # print("CALC MAX UCB")
    # print("UCB NODE CALC: " + tree[str(node)])
    # print("PARENT UCB NODE CALC: " + tree.get(node)[0])

    if visits == 0:
        UCB = math1.inf
    else:
        UCB = (value / visits) + C * math1.sqrt(math1.log(parentNodeVisits) / visits)

    # print("UCB Calculated as: " + str(UCB))
    return UCB


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
            # print("DRAW FOUND: " + str(state))
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


def printTree():
    global tree
    keys = tree.keys()
    values = tree.values()
    for k, v in zip(keys, values):
        print(k)
        print("      " + str(v))
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
