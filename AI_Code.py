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


def MCTS(state):
    global tree
    tree.clear()
    og_state = [init_board, state[1]]
    # store intitial state, storing total number of nodes and times visited
    tree[str(og_state)] = ['start', 0, 0, 0]  # dict to store node info: parent, t, n, RAVE

    # add first node
    tree[str(state)] = [str(og_state), 0, 0, 0]

    # set a timeout
    timeout = 15
    start = timer.time()

    # Run MCTS
    while timer.time() < start + timeout:
        # Expand the tree
        traverse_and_expand(state)

    print("tree: " + str(tree))
    # At end of loop identify successors
    succ = successors(state)

    # Apply UCB formula to all successors #TODO change this to RAVE
    maxRAVE = -math1.inf
    bestNextState = succ[0]
    print("successors: " + str(succ))
    for s in succ:
        # thisUCB = calcUCB(s)
        RAVE = int(tree[str(s)][3])
        if RAVE > maxRAVE:
            maxRAVE = RAVE
            bestNextState = s
    # Return best state
    return bestNextState


def calcUCB(node):
    global tree
    C = 2
    # if empty node make it inf else apply UCB1 formula
    if tree[str(node)][1] == 0 and tree[str(node)][2] == 0:
        UCB = math1.inf
    else:
        # apply UCB
        UCB = int(tree[str(node)][1]) + C * math1.sqrt(
            (math1.log(int(tree[str(tree[str(node)][0])][2]) / int(tree[str(node)][2]))))

    return UCB


def updateRaveValues(rollouts):
    global tree
    print("UPDATING RAVE VALUES...")
    for roll in rollouts:
        #print("winning rollout: " + str(roll))
        rollout_value = roll[0]
        nodesEncountered = roll[1]
        for node in nodesEncountered:
            if str(node) in tree:
                print("NODE FOUND: " + str(node))
                print("N[2] & RAVE[3]: " + str(tree[str(node)]))
                N = int(tree[str(node)][2])  # number of times node is visited
                RAVE = int(tree[str(node)][3])  # rave value from tree
                print("PREVIOUS RAVE VALUE: " + str(tree[str(node)][3]))
                tree[str(node)][3] = str((RAVE * N + rollout_value) / (N + 1))  # updateRaveValue
                print("UPDATED RAVE VALUE: " + str(tree[str(node)][3]))
                tree[str(node)][2] = str(int(tree[str(node)][2]) + 1)
                print("UPDATED N VALUE: " + str(tree[str(node)][2]))
            else:

                #print("nodeEncountered: " + str(nodesEncountered[0]))
                #print("tree: " + str(tree))
                print("NODE NOT FOUND IN TREE")


def successors(state):
    to_move = state[1]

    if to_move == 1:
        to_move = 'X'
    else:
        to_move = 'O'

    if state[1] == 1:
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
    global board_size
    current_board = state[0]
    dim = len(current_board)

    winner = None
    winner_found = False
    while not winner_found:
        # checks all horizontal wins
        for i in range(dim):
            for j in range(dim - 5):
                if current_board[i][j] == current_board[i][j + 1] == current_board[i][j + 2] == current_board[i][
                    j + 3] == current_board[i][j + 4]:
                    winner = current_board[i][j]
                    winner_found = True
        # checks vertical wins
        for i in range(dim - 5):
            for j in range(dim):
                if current_board[i][j] == current_board[i + 1][j] == current_board[i + 2][j] == current_board[i + 3][
                    j] == current_board[i + 4][j]:
                    winner = current_board[i][j]
                    winner_found = True

        # checks diagonal wins
        i = 4
        while i < board_size:
            j = 0
            while j < board_size - 4:
                if current_board[i][j] == current_board[i - 1][j + 1] == current_board[i - 2][j + 2] == \
                        current_board[i - 3][j + 3] == current_board[i - 4][j + 4]:
                    winner = current_board[i][j]
                    winner_found = True

                j += 1
            i += 1

        # checks other diagonals
        i = 4
        while i < board_size:
            j = 4
            while j < board_size:
                if current_board[i][j] == current_board[i - 1][j - 1] == current_board[i - 2][j - 2] == \
                        current_board[i - 3][j - 3] == current_board[i - 4][j - 4]:
                    winner = current_board[i][j]
                    winner_found = True

                j += 1
            i += 1
        draw_found = True
        for i in range(len(current_board)):
            for j in range(len(current_board)):
                if current_board[i][j] != 'X' and current_board[i][j] != 'O':
                    draw_found = False
        if draw_found:
            winner = 0
            return True, winner, []

        winner_found = True

    if winner == "X":
        winner = 1
        return True, winner, []
    elif winner == "O":
        winner = -1
        return True, winner, []

    winner = 2
    return False, winner, []


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
    n = random.randint(1, 6)  # performs n many rollouts
    print("n: " + str(n))
    rolloutSim = rollout(state)  # first rollout
    rollouts = [rolloutSim]
    for i in range(n):
        nextRollout = rollout(state)

        if rolloutSim[0] > nextRollout[0] and turn == 1:
            rolloutSim = nextRollout
        elif rolloutSim[0] < nextRollout[0] and turn == 0:
            rolloutSim = nextRollout

        rollouts.append(rolloutSim)

    updateRaveValues(rollouts)
    print("rolloutSim" + str(rolloutSim))
    if(len(rolloutSim[1]) == 0):
        return rolloutSim[0], [state]
    else:
        return rolloutSim[0], rolloutSim[1][0]


def backpropagate(node, rolloutValue):
    global tree
    current = node
    while tree[str(current)][0] != "start":
        tree[str(current)] = [tree[str(current)][0], str(int(tree[str(current)][1]) + int(rolloutValue)),
                              str(int(tree[str(current)][2]) + 1), str(tree[str(current)][3])]
        current = tree[str(current)][0]  # current becomes parent node


def isLeaf(node):
    # check if there is a successor state
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
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
    maxRAVE = -math1.inf
    # while current node isn't a leaf node
    while not isLeaf(current):
        print("wow the current node isnt a leaf!")
        # Generate successors
        succ = successors(current)
        # print("succ")
        # print(succ)
        # print("current: " + str(current))
        for s in succ:
            # Add each successor to the tree dictionary
            tree[str(s)] = [current, 0, 0, 0]  # adding successors to tree parent, t, n, RAVE
            # print(tree)
            # Calculate UCB
            # UCB = calcUCB(s)
            RAVE = tree[str(s)][3]
            # If the value for this node is greater, then set it to be the chosen node
            if (RAVE > maxRAVE):  # select node which maximises UCB1 #TODO i have changed this
                maxRAVE = RAVE
                RAVENode = s

        # Change current node
        current = RAVENode

    # current is a leaf node
    # if the node hasn't been visited, don't expand
    if (tree[str(current)][1] == 0):  # ni value for node is 0

        # Use MCR to determine a value
        print("current is leaf node and hasn't been visited")
        value = MCR_player(current)[0]  # rollout value
        # print("hi")

        # Once we have the value, backpropogate upwards
        backpropagate(current, value)
        # print("goodbye")

    # if the node has been visted, expand and add to tree
    else:
        # Recursively runs until a leaf is found
        succ = successors(current)
        for s in succ:
            tree[str(s)] = [current, 0, 0, 0]  # adding successors to tree
        current = succ[0]  # current = first new child node
        print("current is leaf node and has been visited")
        value = MCR_player(current)[0]  # rollout value
        backpropagate(current, value)
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
