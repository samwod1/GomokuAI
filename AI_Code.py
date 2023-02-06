#returns the best possible action to do with that board
import copy
import random

import timer
import initialise
import math as math1

tree = {}
og_state = copy.deepcopy(initialise.board)
board_size = copy.deepcopy(initialise.board_size)
def add_XO_AI(board, to_move):
    cboard = copy.deepcopy(board)
    state = state_conversion(cboard, to_move)

    action = MCTSPlayer(state)

    return action

def state_conversion(board, to_move):
    if to_move == 'X':
        return [board, 1]
    else:
        return [board, 0]


def MCTSPlayer(state):

    print("Starting MCTS")
    start = timer.time()
    action = MCTS(state)
    end = timer.time()
    duration = end-start
    print("")
    print("AI player moved to state: " + str(action))
    print("In time: " + str(duration))

    return action

def MCTS(state):

    tree[str(state)] = ["start", 0, 0] #initial tree node (parent, value, visits)

    iterations = 0
    while iterations < 10:
        traverse_and_expand(copy.deepcopy(state))
        iterations += 1

    succ = successors(copy.deepcopy(state))



def traverse_and_expand(state):
    global tree
    current = state.copy()
    maxUCB = -1 * math1.inf

    while not isLeaf(state):
        succ = successors(current)

        for s in succ:
            #add successors to the tree
            tree[str(s)] = [str(current), 0, 0]
            #calcuate ucb for successor
            UCB = calcUCB(s)
            if UCB > maxUCB:
                maxUCB = UCB
                UCBNode = copy.deepcopy(s)

        current = UCBNode

    if tree[str(current)][2] == 0:
        value = MCR_Player(copy.deepcopy(current))[0]

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




def isLeaf(state):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    #  print("treeValues: " + str(treeValues))
    for i in range(len(treeValues)):
        if treeValues[i][0] == state:
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
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
        return True, 1, []
    elif winner == 'O':
        return True, -1, []

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


def calcUCB(state):
    C = 2
    # if empty node make it inf else apply UCB1 formula
    if tree[str(state)][1] == 0 and tree[str(state)][2] == 0:
        UCB = math1.inf
    else:
        # apply UCB, made first parameter negative
        UCB = -(int(tree[str(state)][1])) + C * math1.sqrt((math1.log(int(tree[str(tree[str(state)][0])][2]) / int(tree[str(state)][2]))))

    print("calcUCB: " + str(UCB))
    return UCB








