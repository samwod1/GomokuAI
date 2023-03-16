# library imports
import math as m
import time

# File Imports
from AI import *

tree = {}
C = m.sqrt(2)
time_limit = 2


def AI_play(board, to_move):
    cbord = copy.deepcopy(board)
    state = state_conversion(cbord, to_move)
    print("AI operating on state: " + str(state))
    state = MCTSInit(state)
    action = stateToAction(cbord, state)
    print("returning action: " + str(action))

    if action is not None:
        return action
    else:
        return [[]]


def MCTSInit(state):
    print("Starting MCTS\n")
    action = MCTS(state)
    print("")
    print("AI player moved to state: " + str(action))

    return action


def MCTS(state):
    global C, tree

    tree.clear()
    tree["('[]', 'start')"] = ['start', 0, 0]
    tree[str((state, '[]'))] = [('[]', 'start'), 0, 0]
    current = (state, '[]')

    start = time.time()
    while time.time() < start + time_limit:
        expand(current)
        # printTree()

    maxUCB = -m.inf
    succ = successors(state)
    C = 0
    UCBNode = []

    for s in succ:
        UCB = calcMaxUCB((s, current[0]))
        if UCB > maxUCB:
            maxUCB = UCB
            UCBNode = s

    return UCBNode


def expand(node):
    global tree
    current = node[:]
    terminalBool = False
    while True:
        node = current[0]
        boolean, value, path = terminal_test(node)
        if boolean:
            terminalBool = True
            break  # stops if the current node is terminal

        if checkLeaf(current):
            break

        maxUCB = -m.inf

        succ = successors(node)
        UCBNode = []
        for s in succ:
            UCB = calcMaxUCB((s, node))
            if UCB == m.inf:
                UCBNode = s
                break
            if UCB > maxUCB:
                maxUCB = UCB
                UCBNode = s

        current = (UCBNode, node)

    if not terminalBool:  # checks if the traversal stopped because a terminal leaf
        if tree[str(current)][2] == 0:
            value = MCR(node)
            backpropagation(current, value)
        else:
            succ = successors(node)
            for s in succ:
                if tree.get(str((s, node))) is None:
                    tree[str((s, node))] = [current, 0, 0]
            firstChild = succ[0]
            value = MCR(firstChild)
            backpropagation((firstChild, node), value)
    else:
        boolean, value, path = terminal_test(node)
        backpropagation(current, value)


def MCR(state):
    return rollout(state)


def backpropagation(node, rolloutValue):
    global tree
    current = node[:]
    while tree[str(current)][0] != "start":
        if current[0][1] == 0:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue * -1),
                                  int(tree[str(current)][2]) + 1]
        else:
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue),
                                  int(tree[str(current)][2]) + 1]

        current = tree[str(current)][0][:]


def checkLeaf(node):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    for i in range(len(treeValues)):
        if treeValues[i][0] == node:
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    return leafBool


def calcMaxUCB(current):
    global tree
    node = tree.get(str(current))
    parentNodeVisits = tree[str(node[0])][2]
    visits = node[2]
    value = node[1]

    if visits == 0:
        UCB = m.inf
    else:
        UCB = (value / visits) + C * m.sqrt(m.log(parentNodeVisits) / visits)

    return UCB


def printTree():
    global tree
    keys = tree.keys()
    values = tree.values()
    for k, v in zip(keys, values):
        print(k)
        print("      " + str(v))
