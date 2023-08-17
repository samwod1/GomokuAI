# library imports
import math as m
import time

# File Imports
from AI import *

tree = {}  # initialise tree as dictionary
C = m.sqrt(2)  # initialise the search constant as the square root of 2, though larger time limit will prefer a lower C
time_limit = setTimeLimit()  # sets limit according to the board size


# The function that links to the Game file
# initiates the MCTSInit func, converts the board to an action
# and returns it
def AI_play(action, to_move):
    state = copy.deepcopy(stateConversion(action, to_move))  # converts the action to a board and makes deepcopy
    print("AI operating on state: " + str(state))
    state = MCTSInit(state)  # initiates the MCTS, which returns a state
    action = stateToAction(action, state)  # uses the state and returns the board with the action applied
    print("returning action: " + str(action))

    if action is not None:  # checks if action is not None and returns it if not returns empty board
        return action
    else:
        return [[]]


# initiates MCTS and returns the board the AI chooses
def MCTSInit(state):
    print("Starting MCTS\n")
    action = MCTS(state)
    print("")
    print("AI player moved to state: " + str(action))

    return action


# initialises the root node in the tree
# starts the time-out and starts the expansion phase
# then carries out the selection phase and returns the AI's decision
def MCTS(state):
    global C, tree

    tree.clear()
    tree["('[]', 'start')"] = ['start', 0, 0]  # initialises the tree with a dummy node at the top
    tree[str((state, '[]'))] = [('[]', 'start'), 0, 0]  # node = [(parent, parent's parent), value, visits]
    current = (state, '[]')  # sets root node as the current

    start = time.time()  # initiates the time limit
    while time.time() < start + time_limit:
        expand(current)  # expansion phase

    # selection phase

    maxUCB = -m.inf  # sets maxUCB to negative infinity
    succ = successors(state)
    C = 0  # sets C to 0 to only consider exploitation and not exploration
    UCBNode = []

    for s in succ:
        UCB = calcMaxUCB((s, current[0]))
        if UCB > maxUCB:
            maxUCB = UCB
            UCBNode = s

    return UCBNode  # returns the AI's decision


# expansion phase of MCTS
# searches the tree until it finds a leaf or a terminal node
# if the leaf is visited it adds its children to the tree and rollouts out from the first child and backpropagates
# if it's not visited it rolls out from the leaf and backpropagates the rollout value
# if the leaf is terminal it backpropagates the terminal value.
def expand(node):
    global tree
    current = node[:]  # sets current to a copy of the passed in node
    terminalBool = False
    while True:
        node = current[0]
        boolean, value, path = terminalTest(node)
        if boolean:
            terminalBool = True
            break  # stops if the current node is terminal

        if checkLeaf(current):
            break  # stops if current is a leaf

        # finds the maximum UCB for the child nodes in the tree and moves down the tree
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

        current = (UCBNode, node)  # sets current to the chosen node and repeats process

    if not terminalBool:  # checks if the traversal stopped because a terminal leaf
        if tree[str(current)][2] == 0:  # if visits == 0
            value = MCR(node)  # rolls out from node
            backpropagation(current, value)  # backpropagates rollout value from current
        else:  # if not visited
            succ = successors(node)  # generates successors
            for s in succ:
                if tree.get(str((s, node))) is None:
                    tree[str((s, node))] = [current, 0, 0]  # adds successors to the tree
            firstChild = succ[0]
            value = MCR(firstChild)  # rolls out from first child
            backpropagation((firstChild, node), value)  # backpropagates rollout value from firstChild
    else:  # if the leaf is terminal then terminal value is backpropagated
        boolean, value, path = terminalTest(node)
        backpropagation(current, value)


# returns the rollout from the state
def MCR(state):
    return rollout(state)


# backpropagates up the tree using adding 1 to visits and adding rolloutValue to the node value
def backpropagation(node, rolloutValue):
    global tree
    current = node[:]
    while tree[str(current)][0] != "start":  # loops all the way up to dummy node then stops
        if current[0][1] == 0:  # if the current node is a max node the value is negated, as the parent is a min node
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue * -1),
                                  int(tree[str(current)][2]) + 1]
        else:  # if the current node is a min node the value is normal because the parent is a max node
            tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue),
                                  int(tree[str(current)][2]) + 1]

        current = tree[str(current)][0][:]  # sets current as a copy of the tree node


# returns a bool if the node is a leaf
def checkLeaf(node):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())  # returns tuple of all the tree values
    for i in range(len(treeValues)):  # goes through all the tree values
        if treeValues[i][0] == node:  # if the parent of the node is the current then
            leafBool = False
            break
    return leafBool


# takes a node and gets the UCB1 value of it
def calcMaxUCB(current):
    global tree
    node = tree.get(str(current))
    parentNodeVisits = tree[str(node[0])][2]
    visits = node[2]
    value = node[1]

    if visits == 0:
        UCB = m.inf
    else:
        UCB = (value / visits) + C * m.sqrt(m.log(parentNodeVisits) / visits)  # the UCB1 formula

    return UCB
