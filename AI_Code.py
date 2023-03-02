# returns the best possible action to do with that board
import copy
import random

import time
import initialise
import math as math1

tree = []
og_state = copy.deepcopy(initialise.board)
board_size = initialise.board_size
winCondition = initialise.winCondition
blackWins = 0
whiteWins = 0
draws = 0
C = 0
total_iterations = 0


class Node:
    def __init__(self, node, parent, parent_pos, pos, value, visits):
        self.node = node
        self.parent = parent
        self.parent_pos = parent_pos
        self.pos = pos
        self.value = value
        self.visits = visits


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
    start = time.time()
    action = MCTS(state)
    end = time.time()
    duration = end - start
    print("")
    print("AI player moved to state: " + str(action))
    print("In time: " + str(duration))

    return action


def createNode(state, parent, parent_pos):
    global tree
    node = Node(state, parent, parent_pos, len(tree), 0, 0)
    tree.append(node)
    return node


def MCTS(state):
    global C, tree, blackWins, whiteWins, draws
    blackWins = 0
    whiteWins = 0
    draws = 0

    tree.clear()
    createNode([], "start", -1)  # create the root node
    start = createNode(state, [], 0)  # create the initial node
    start.visits = 1
    iterations = 0
    C = 1.4

    while iterations <= 1000:
        traverse_and_expand()
        # printPartialTree()
        printTree()
        input("Press enter to continue...")
        iterations += 1

    maxUCB = -math1.inf

    succ = successors(start.node)
    UCBNode = copy.deepcopy(succ[0])
    C = 0

    for s in succ:
        UCB = calcMaxUCB(s, start.node)
        if UCB > maxUCB:
            maxUCB = UCB
            UCBNode = copy.deepcopy(s)

    print("Black Wins: " + str(blackWins))
    print("White Wins: " + str(whiteWins))
    print("Draws: " + str(draws))

    return UCBNode


def traverse_and_expand():
    current = copy.deepcopy(tree[1])
    terminalBool = False
    while True:
        boolean, value, path = terminal_test(current.node)
        if boolean:
            terminalBool = True
            break

        print("Current  " + printNodeValues(current))
        if isLeaf(current):
            break


        maxUCB = -math1.inf
        minUCB = math1.inf

        succ = successors(copy.deepcopy(current.node))

        # for s in succ:
        #     UCB = calcMaxUCB(s, current.node)
        #     if UCB == math1.inf:
        #         UCBNode = s
        #         break
        #     if UCB > maxUCB:
        #         maxUCB = UCB
        #         UCBNode = s

        if current.node[1] == 0:
            print("CALCULATING SUCCESSOR MAX UCB")
            for s in succ:
                UCB = calcMaxUCB(s, current.node)
                if UCB == math1.inf:
                    UCBNode = copy.deepcopy(s)
                    break
                if UCB > maxUCB:
                    maxUCB = UCB
                    UCBNode = copy.deepcopy(s)

        else:
            print("CALCULATING SUCCESSOR MIN UCB")
            for s in succ:
                UCB = calcMinUCB(s, current.node)
                if UCB == -math1.inf:
                    UCBNode = copy.deepcopy(s)
                    break
                if UCB < minUCB:
                    minUCB = UCB
                    UCBNode = copy.deepcopy(s)

        current = copy.deepcopy(getNode(copy.deepcopy(UCBNode), current.node))
    if not terminalBool:
        if current.visits == 0:
            print("Leaf has no visits \n")
            value = MCR_player(current.node)
            backpropagate(current, value)
        else:
            print("Leaf has been visited\n")
            succ = successors(current.node)
            parent_pos = current.pos
            if len(succ) != 0:
                print("Rolling out on first child: " + str(succ[0]))
                for s in succ:
                    createNode(s, current.node, parent_pos)

                # index = random.randint(0, len(succ) - 1)
                # print("rollout chooses: " + str(succ[index]))
                # state = copy.deepcopy(succ[index])  # print("picking: " + str(succ[index]))
                firstChild = getNode(succ[0], current.node)
                value = MCR_player(firstChild.node)
                backpropagate(firstChild, value)
    else:
        print("Leaf node is terminal: " + str(current.node) + "\n")
        print("No rollout needed, backpropagating utility")
        boolean, value, path  = terminal_test(current.node)
        backpropagate(current, value)


def getNode(child, parent):
    for i in range(len(tree)):
        if tree[i].node == child and tree[i].parent == parent:
            return tree[i]


def getParent(parent_pos):
    return tree[parent_pos]


def printNodeValues(node):
    return ("node: " + str(node.node) + " parent: " + str(node.parent) +
            " parent_pos: " + str(node.parent_pos) + " value: " + str(node.value) + " visits: " + str(node.visits))


def printBoard(n):
    node = n[0]
    board = ""
    # print("node: " + str(node))
    for i in range(len(node)):
        board = board + "| "
        for j in range(len(node)):
            if node[i][j] == 'O' or node[i][j] == 'X':
                board = board + (" " + str(node[i][j]) + " ")
            else:
                board = board + " _ "
    board = board + "|"
    return board


def printNode(node):
    string = ""
    string = string + str(getDepth(node))
    string = string + (
            str(printBoard(node.node)) + "turn: " + str(node.node[1]) + " visits: " + str(node.visits) + " value: "
            + str(node.value) + " maxUCB: " + str(calcMaxUCB(node.node, node.parent)) if node.parent != [] else
            str("UCB: N/A"))
    #     " UCB: N/A")))
    # (" maxUCB: " + str(calcMaxUCB(node.node, node.parent)) if node.parent[1] == 0 else str(
    #     " minUCB: " + str(calcMinUCB(node.node, node.parent)))) if node.parent != [] else str(
    #     " UCB: N/A")))
    return string


def getChildren(node):
    children = []
    for i in range(len(tree)):
        if tree[i].parent_pos == node.pos:
            if tree[i] != None:
                children.append(tree[i])

    return children


def getDepth(node):
    current = copy.deepcopy(node)
    depth = 0
    while current.parent != "start":
        depth += 1
        current = getParent(current.parent_pos)

    return depth


def printTree():
    print("<<TREE>>")
    print(" C = " + str(C))
    printTreeRecursive(tree[1])


def printTreeRecursive(node):
    children = getChildren(node)
    print(str(getDepth(node)), end=". ")
    print(str(printBoard(node.node)) + "turn: " + str(node.node[1]) + " visits: " + str(node.visits) + " value: "
          + str(node.value) + " maxUCB: " + str(calcMaxUCB(node.node, node.parent)) if node.parent != [] else str(
        " UCB: N/A"))

    # ((" maxUCB: " + str(calcMaxUCB(node.node, node.parent)) if node.parent[1] == 0
    #   else str(" minUCB: " + str(calcMinUCB(node.node, node.parent)))) if node.parent != [] else str(
    #     " UCB: N/A")))
    for c in children:
        printTreeRecursive(c)


def printPartialTree():
    global tree
    print("<<TREE>>")
    print(" C = " + str(C))
    children = getChildren(tree[1])
    for c in children:
        s = printNode(c)
        if s is not None:
            print(s)


def MCR_player(state):
    return rollout(state)
    # turn = state[1]
    # n = 5  # performs n many rollouts
    # rolloutSim = rollout(state)  # first rollout
    #
    # for i in range(n):
    #     nextRollout = rollout(state)
    #     if rolloutSim < nextRollout and turn == 0:
    #         rolloutSim = nextRollout
    #     elif rolloutSim > nextRollout and turn == 1:
    #         rolloutSim = nextRollout
    #
    # return rolloutSim

    # result = rollout(state)
    # if state[1] == 0:
    #     return result * -1
    # elif state[1] == 1:
    #     return result


def backpropagate(firstChild, value):
    global tree
    currentNode = copy.deepcopy(firstChild)
    print("BACK PROPAGATING FROM  " + printNodeValues(currentNode))
    print("AT DEPTH: " + str(getDepth(currentNode)))
    while currentNode.parent != "start":
        for i in range(len(tree)):
            if tree[i].node == currentNode.node and tree[i].parent == currentNode.parent:
                tree[i] = Node(tree[i].node, tree[i].parent, tree[i].parent_pos, tree[i].pos, tree[i].value + value,
                            tree[i].visits + 1)


                parent = copy.deepcopy(tree[i])
                print("UPDATING NODE VALUES  " + printNodeValues(tree[i]))
        parent = getParent(parent.parent_pos)
        print("SWITCHING TO PARENT  " + printNodeValues(parent))
        currentNode = parent
    print("BACKPROPAGATION FINISHED\n")


def rollout(s):
    global draws, blackWins, whiteWins
    state = copy.deepcopy(s)
    print("ROLLOUT COMMENCING FROM: " + str(state))
    while True:
        terminal, utility, path = terminal_test(state)
        if terminal:
            print("ROLLOUT FINISHED AT STATE: " + str(state))
            print("WITH UTILITY:" + str(utility) + "\n")
            if utility == 0:
                draws += 1
            elif utility == 1:
                whiteWins += 1
            elif utility == -1:
                blackWins += 1

            return utility
        else:
            succ = successors(state)
            # print("rollout successors: " + str(succ))
            index = random.randint(0, len(succ) - 1)
            # print("rollout chooses: " + str(succ[index]))
            state = copy.deepcopy(succ[index])  # print("picking: " + str(succ[index]))


def isLeaf(state):
    global tree
    print("CHECKING IF LEAF")
    leafBool = True
    for i in range(len(tree)):
        # print("tree node: " + printNodeValues(tree[i]))
        # print("parent: " + printNodeValues(state))
        if str(tree[i].parent) == str(state.node):
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    if leafBool:
        print("LEAF FOUND: " + str(state.node))
    else:
        print("NOT LEAF: " + str(state.node))

    return leafBool


def calcMinUCB(s, parent):
    node = getNode(s, parent)
    parentNode = getParent(node.parent_pos)
    # print("CALC MIN UCB")
    # print("UCB NODE CALC: " + printNodeValues(node))
    # print("PARENT UCB NODE CALC: " + printNodeValues(parentNode))

    if node.visits == 0:
        UCB = -math1.inf
    else:
        UCB = (node.value / node.visits) - C * math1.sqrt(math1.log(parentNode.visits) / node.visits)

    # print("UCB Calculated as: " + str(UCB))

    return UCB


def calcMaxUCB(s, parent):
    node = getNode(s, parent)
    parentNode = getParent(node.parent_pos)
    # print("CALC MAX UCB")
    # print("UCB NODE CALC: " + printNodeValues(node))
    # print("PARENT UCB NODE CALC: " + printNodeValues(parentNode))

    if node.visits == 0:
        UCB = math1.inf
    else:
        UCB = (node.value / node.visits) + C * math1.sqrt(math1.log(parentNode.visits) / node.visits)

    # print("UCB Calculated as: " + str(UCB))
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
