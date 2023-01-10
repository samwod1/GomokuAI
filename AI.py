import copy
import math as math1
import random
import time as timer

import pygame
import Game
import initialise

tree = {}
board_size = initialise.board_size
init_board = initialise.board
BOARD_SIZE = initialise.BOARD_SIZE
actions = []


def MCTS(state):
    global tree, actions
    tree.clear()
    og_state = [init_board, state[1]]
    #populate the actions list
    for i in range(board_size*board_size):
        actions.append([0, 0]) #RAVE value, N

    # store intitial state, storing total number of nodes and times visited
    tree[str(og_state)] = ['start', 0, 0]  # dict to store node info: parent, t, n, RAVE

    # add first node
    tree[str(state)] = [str(og_state), 0, 0]

    # set a timeout
    timeout = 15
    start = timer.time()

    # Run MCTS
    while timer.time() < start + timeout:
        # Expand the tree
        traverse_and_expand(state)

    #print("tree: " + str(tree))
    # At end of loop identify successors
    succ = successors(state)

    # Apply UCB formula to all successors #TODO change this to RAVE
    maxRAVE = -math1.inf
    bestNextState = succ[0]
    #print("successors: " + str(succ))
    for s in succ:
        # thisUCB = calcUCB(s)
        RAVE = raveValueOfSuccessor(state, s)[0]
        if RAVE > maxRAVE:
            maxRAVE = RAVE
            bestNextState = s

    print("MCTS  Stage has chosen the state: " + str(bestNextState) + " with RAVE value: " + str(maxRAVE))

    # Return best state
    return bestNextState

#takes the original state and a successor of it and determines the tile
#that the successor took action on
def raveValueOfSuccessor(state, successor):
    actionsIndex = -1
    state = state[0]
    successor = successor[0]
    RAVE = actions[actionsIndex]
    for i in range(len(state)):
        for j in range(len(state[0])):
            actionsIndex += 1
            if state[i][j] != successor[i][j]:
                RAVE = actions[actionsIndex]
                break

    return RAVE

def updateRaveValues(rollouts):
    global tree, actions
    print("UPDATING RAVE VALUES")
    #print("rollout: " + str(rollouts[0]))
    for rollout in rollouts:
        rollout_value = rollout[0]
        best_path = rollout[1]
        final_state = rollout[1][len(best_path) - 1][0]
        pos = -1

        for i in range(len(final_state)):
            for j in range(len(final_state[0])):
                pos += 1
                if final_state[i][j] == 'X' or final_state[i][j] == 'O':
                    RAVE = actions[pos][0]
                    N = actions[pos][1]
                    actions[pos][0] = (RAVE * N + rollout_value) / (N + 1)
                    actions[pos][1] = (N + 1)

    print("ACTIONS: " + str(actions))

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
            next_state = copy.deepcopy(current_board)
            if next_state[i][j] != 'X' and next_state[i][j] != 'O':
                next_state[i][j] = to_move
                res.append([next_state, to_move_num])

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
    n = random.randint(1, 10)  # performs n many rollouts
    print("PERFORMING " + str(n) + " ROLLOUTS...")
    rolloutSim = rollout(state)  # first rollout
    rollouts = [rolloutSim]
    for i in range(n):
        nextRollout = rollout(state)

        if rolloutSim[0] > nextRollout[0] and turn == 1:
            rolloutSim = nextRollout
        elif rolloutSim[0] < nextRollout[0] and turn == 0:
            rolloutSim = nextRollout

        rollouts.append(rolloutSim)

    updateRaveValues(rollouts) #sends final rollout to update the RAVE values via the actions
    if(len(rolloutSim[1]) == 0):
        return rolloutSim[0], [state]
    else:
        return rolloutSim[0], rolloutSim[1][0]


def backpropagate(node, rolloutValue):
    global tree
    current = node
    while tree[str(current)][0] != "start":
        tree[str(current)] = [tree[str(current)][0], str(int(tree[str(current)][1]) + int(rolloutValue)),
                              str(int(tree[str(current)][2]) + 1)]
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
        # Generate successors
        succ = successors(current)
        for s in succ:
            # Add each successor to the tree dictionary
            tree[str(s)] = [current, 0, 0]  # adding successors to tree parent, t, n

            RAVE = raveValueOfSuccessor(node, s)[0]
            # If the value for this node is greater, then set it to be the chosen node
            if RAVE > maxRAVE:  # select node which maximises UCB1 #TODO i have changed this
                maxRAVE = RAVE
                RAVENode = s

        # Change current node
        current = RAVENode

    print("Traverse and Expand Stage has chosen the state: " + str(current) + " with RAVE value: " + str(maxRAVE))

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

    Game.render_board(current_board, X_IMG, O_IMG)

    for i in range(board_size):
        for j in range(board_size):
            if current_graphical_board[i][j][0] is not None:
                SCREEN.blit(current_graphical_board[i][j][0], current_graphical_board[i][j][1])

    pygame.display.update()

    return current_board, to_move
