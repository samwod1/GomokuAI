# library imports
import copy
import time
import math as math1

# File Imports
import Initialise
from AI import *

tree = {}
board_size = Initialise.board_size
winCondition = Initialise.winCondition
blackWins = 0
whiteWins = 0
draws = 0
C = 0
total_iterations = 0
time_limit = 12


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
        if UCB > maxUCB:  # input("press enter")

            maxUCB = UCB
            UCBNode = s

    # print("Black Wins: " + str(blackWins))
    # print("White Wins: " + str(whiteWins))
    # print("Draws: " + str(draws))

    return UCBNode


def traverse_and_expand(node):
    global tree
    current = node[:]
    # current = [[x for x in row] for row in node]
    terminalBool = False
    while True:
        node = current[0]
        parent = current[1]
        boolean, value, path = terminal_test(node)
        if boolean:
            terminalBool = True
            break  # stops if the current node is terminal

        # print("Current  " + str(tree.get(str(current))))
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

        current = (UCBNode, node)

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
    current = node[:]
    # current = [row[:] for row in node]
    # print("backpropagating")
    while tree[str(current)][0] != "start":
        if current[0][1] == 0:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue * -1),
                                  int(tree[str(current)][2]) + 1]
        else:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue),
                                  int(tree[str(current)][2]) + 1]

        current = tree[str(current)][0][:]


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


def printTree():
    global tree
    keys = tree.keys()
    values = tree.values()
    for k, v in zip(keys, values):
        print(k)
        print("      " + str(v))

