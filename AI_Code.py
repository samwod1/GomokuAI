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
    tree.clear()
    og_state = [init_board, state[1]]

    # store intitial state, storing total number of nodes and times visited
    tree[str(og_state)] = ['start', 0, 0]  # dict to store node info: parent, t, n

    # add first node
    tree[str(state)] = [og_state, 0, 0]

    # set a timeout
    timeout = 15
    start = timer.time()
    iterations = 0

    # Run MCTS
    while iterations < 5:
        # Expand the tree
        traverse_and_expand(state)
        iterations += 1

    #checks if the tree is empty
    print("tree: " + str(tree))
    # At end of loop identify successors
    succ = successors(state)

    # Apply UCB formula to all successors
    maxUCB = -math1.inf
    bestNextState = succ[0]
    for s in succ:
        print("Successor: " + str(s))
        thisUCB = calcUCB(s)
        print("UCB: " + str(thisUCB))
        if thisUCB > maxUCB:
            print("thisUCB: " + str(thisUCB) + " is greater than " + str(maxUCB))
            maxUCB = thisUCB
            bestNextState = s
    print("MCTS has chosen: " + str(bestNextState))
    return bestNextState
    # Return best state

def calcUCB(node):
    global tree
    C = 2
    # if empty node make it inf else apply UCB1 formula
    if tree[str(node)][1] == 0 and tree[str(node)][2] == 0:
        UCB = math1.inf
    else:
        # apply UCB
        UCB = int(tree[str(node)][1]) + C * math1.sqrt((math1.log(int(tree[str(tree[str(node)][0])][2]) / int(tree[str(node)][2]))))

    print("calcUCB: " + str(UCB))
    return UCB


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
        return True, 1, []
    elif winner == 'O':
        return True, -1, []

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

    turn = state[1]
    n = random.randint(1, 20)  # performs n many rollouts
    # print("n: " + str(n))
    rolloutSim = rollout(state)  # first rollout

    for i in range(n):
        nextRollout = rollout(state)
        if rolloutSim[0] > nextRollout[0] and turn == 1:
            rolloutSim = nextRollout
        elif rolloutSim[0] < nextRollout[0] and turn == 0:
            rolloutSim = nextRollout

    # print("rolloutSim" + str(rolloutSim))

    if len(rolloutSim[1]) == 0:
        return rolloutSim[0], [state]
    else:
        return rolloutSim[0], rolloutSim[1][0]


def backpropagate(node, rolloutValue):
    global tree
    current = node
    while tree[str(current)][0] != "start":
        tree[str(current)] = [tree[str(current)][0], int(tree[str(current)][1]) + int(rolloutValue), int(tree[str(current)][2]) + 1]
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


def traverse_and_expand(node):
    # Function to travel the tree and expand it
    global tree
    current = node
    maxUCB = -math1.inf
    # while current node isn't a leaf node
    while not isLeaf(current):
        print("Current is not a leaf!")
        # Generate successors
        succ = successors(current)
        print("current: " + str(current))
        print("succ: " + str(succ))
        for s in succ:
            # Add each successor to the tree dictionary
            if tree.get(str(s)) is None: #check to see if the successor is already in the tree, so it doesnt overwrite its stats
                tree[str(s)] = [current, 0, 0]  # adding successors to tree
            #print(tree)
            # Calculate UCB
            print("Successor: " + str(s))
            print("Successors Visits: " + str(tree[str(s)][2]))
            print("Successor Value: " + str(tree[str(s)][1]))
            UCB = calcUCB(s)
            print("UCB: " + str(UCB))
            # If the value for this node is greater, then set it to be the chosen node
            if (UCB > maxUCB):  # select node which maximises UCB1
                maxUCB = UCB
                UCBNode = s
                print("maxUCB has changed to! " + str(maxUCB))
                print("UCBNode has changed to! " + str(UCBNode))

        # Change current node
        print("Traverse and Expand has chosen: " + str(UCBNode))
        print("Is UCBNode a leaf node? " + str(isLeaf(UCBNode)))
        current = UCBNode

    # current is a leaf node
    # if the node hasn't been visited, don't expand
    if (tree[str(current)][2] == 0):  # ni value for node is 0
        print("Node hasn't been visited!")
        # Use MCR to determine a value
        value = MCR_player(current)[0]  # rollout value

        # Once we have the value, backpropogate upwards
        backpropagate(current, value)

    # if the node has been visted, expand and add to tree
    else:
        print("Node has been visited!")
        # Recursively runs until a leaf is found
        succ = successors(current)
        for s in succ:
            if tree.get(str(s)) is None:
                tree[str(s)] = [current, 0, 0]  # adding successors to tree

        current = succ[0]  # current = first new child node
        value = MCR_player(current)[0]  # rollout value
        backpropagate(current, value)
    return


def AI_Player_mcts(state):
    start = timer.time()
    game_state = MCTS(state)
    end = timer.time()
    duration = end-start
    print("")
    print("AI player moved to state " + str(game_state))
    print("Time taken: " + str(duration))
    return game_state


def state_conversion(current_board, to_move):
    if to_move == "X":
        state = [current_board, 1]
    else:
        state = [current_board, 0]

    return state


def add_XO_AI(current_board, current_graphical_board, to_move, X_IMG, O_IMG, SCREEN, board_size):
    state = state_conversion(current_board, to_move)

    game_state = AI_Player_mcts(state)

    current_board = game_state[0]

    if game_state[1] == 0:
        to_move = 'O'
    else:
        to_move = 'X'

    Game_Code.render_board(current_board, X_IMG, O_IMG)

    for i in range(board_size):
        for j in range(board_size):
            if current_graphical_board[i][j][0] is not None:
                SCREEN.blit(current_graphical_board[i][j][0], current_graphical_board[i][j][1])

    pygame.display.update()

    return current_board, to_move
