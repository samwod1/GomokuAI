import time
import math
import random
# Monte Carlo Tree Search

# Create an empty tree as a global
tree = {}


def MCTS(state):
    global tree
    # Store initial state, storing total and number of nodes
    tree['[]'] = ['start', 0, 0]  # dict to store node info: parent, t, n

    # Store first node
    tree[str(state)] = ['[]', 0, 0]

    # Set time limit, we set to 10 seconds
    timeout = 10
    start = time.time()

    # Run MCTS
    while (time.time() < start + timeout):
        # Expand the tree
        traverse_and_expand(state)

    # At end of loop identify successors
    succ = successors(state)

    # Apply UCB formula to all successors
    maxUCB = -math.inf
    for s in succ:
        thisUCB = calcUCB(s)
        if (thisUCB > maxUCB):
            maxUCB = thisUCB
            bestNextState = s
    # Return best state
    return bestNextState

# Function to calculate the UCB formula
def calcUCB(node):
    global tree
    C = 2
    # If its an empty node, set to inf, else, apply formula
    if (tree[str(node)][1] == 0 and tree[str(node)][2] == 0):
        UCB =  math.inf
    else:
        # Apply formula
        UCB = int(tree[str(node)][1]) + C * math.sqrt((math.log(int(tree[str(tree[str(node)][0])][2]) / int(tree[str(node)][2]))))
    return UCB

# Same successor generation as before
def successors(state):
    # Function to get all successors for a state, i.e. similar to next states

    succ = []
    # Successor state is the next player, so change turn
    turn = state[1]
    if(turn == 1):
        turn = 2
    else:
        turn = 1

    # Sort piles, i.e. state
    piles = state[0]
    # Go through each pile and generate possible options
    for i in range (len(piles)):

        #  If one or more piles
        #  Could be more efficient I think
        #  Not an ideal solution, but its late
        if(piles[i] != [] and piles[i] >= 1):
            next_succ = piles.copy()
            newValue = piles[i] -1 #remove 1 stick from pile i
            if(newValue == 0):
                next_succ.pop(i) #removing zero index
            else:
                next_succ[i] = newValue
            # Add to the pile
            succ.append((next_succ, turn))
            if(piles[i]>= 2):
                next_succ = piles.copy()
                newValue = piles[i] -2 #remove 2 stick from pile i
                if(newValue == 0):
                    next_succ.pop(i) #removing zero index
                else:
                    next_succ[i] = newValue
                succ.append((next_succ, turn))
                if(piles[i]>= 3):
                    next_succ = piles.copy()
                    newValue = piles[i] -3  #remove 3 stick from pile i
                    if(newValue == 0):
                        next_succ.pop(i) #removing zero index
                    else:
                        next_succ[i] = newValue
                    succ.append((next_succ, turn))

    # replacing list of empty piles with single []
    for i in range(len(succ)):
        # Sort!
        succ[i][0].sort()
        emptyPiles = True
        for k in range(len(succ[i][0])):
            if(succ[i][0][k] == []):
                emptyPiles = emptyPiles and True
            else:
               emptyPiles = emptyPiles and False
        if(emptyPiles):
            succ[i] = ([],turn)
    #removing duplicates from list
    res = []
    for i in succ:
        if i not in res:
            res.append(i)

    # Return the list of successors, possible outcomes
    return(res)

# Same as before
def terminal_test(state):
    # Function to test if goal has been met
    # True if met, false if not
    if (state == ([], 1) or state == ([], 2)):
        return True
    else:
        return False

# same as before
def utility_prune(state):
    # Function to return the utility value in a suitable format
    if (state == ([], 1)):
        return 1, []  # a win for MAX
    elif (state == ([], 2)):
        return -1, []  # a win for MIN

# Functions to do quick MCR rollouts
def rollout(state):
    bestPath = []
    while (True):  # loop unitl terminal state is reached
        if (terminal_test(state)):
            return utility_prune(state)[0], bestPath
        else:
            succ = successors(state)
            index = random.randint(0, len(succ) - 1)
            state = succ[index]
            bestPath.append(state)

# Main rollout function
def MCR_player(state):
    turn = state[1]
    n = random.randint(1, 6)  # prefroms n many rollouts
    rolloutSim = rollout(state)  # first rollout
    for i in range(n - 1):
        nextRollout = rollout(state)
        if (rolloutSim[0] > nextRollout[0] and turn == 2):  # best is -1
            rolloutSim = nextRollout
        elif (rolloutSim[0] < nextRollout[0] and turn == 1):  # best is +1
            rolloutSim = nextRollout
    return rolloutSim[0], rolloutSim[1][0]  # best next move from rollouts

# Back propogate values all the way up the tree
def backpropagate(node, rolloutValue):
    global tree
    current = node
    while(tree[str(current)][0] != 'start'):
        tree[str(current)] = [tree[str(current)][0],str(int(tree[str(current)][1]) + int(rolloutValue)), str(int(tree[str(current)][2]) + 1)]
        current = tree[str(current)][0] #current become parent node

# If check if there is a successor state
def isLeaf(node):
    global tree
    leafBool = True
    treeValues = tuple(tree.values())
    for i in range (len(treeValues)):
        if(treeValues[i][0] == node):
            leafBool = False and leafBool
        else:
            leafBool = True and leafBool
    return leafBool

def traverse_and_expand(node):
    # Function to travel the tree and expand it
    global tree
    current = node
    maxUCB = -math.inf

    # while current node isn't a leaf node
    while (not isLeaf(current)):
        # Generate successors
        succ = successors(current)
        for s in succ:
            # Add each successor to the tree dictionary
            tree[str(s)] = [current, 0, 0]  # adding successors to tree
            # Calculate UCB
            UCB = calcUCB(s)
            # If the value for this node is greater, then set it to be the chosen node
            if (UCB > maxUCB):  # select node which maximises UCB1
                maxUCB = UCB
                UCBNode = s

        # Change current node
        current = UCBNode

    # current is a leaf node
    # if the node hasn't been visited, don't expand
    if (tree[str(current)][1] == 0):  # ni value for node is 0
        # Use MCR to determine a value
        value = MCR_player(current)[0]  # rollout value

        # Once we have the value, backpropogate upwards
        backpropagate(current, value)
    # if the node has been visted, expand and add to tree
    else:
        # Recursively runs until a leaf is found
        succ = successors(current)
        for s in succ:
            tree[str(s)] = [current, 0, 0]  # adding successors to tree
        current = succ[0]  # current = first new child node
        value = MCR_player(current)[0]  # rollout value
        backpropagate(current, value)
    return


# Game creation from previous
# Main function to run game
def Nim():
    # initial variables
    initialState = []
    state = ()

    print("Let's play Nim")

    # Add try catch to ensure only valid values are accepted
    valid = False;
    while valid==False:
        try:
            # Get piles and sticks
            numPiles = input("How many piles initially? ")
            maxSticks = input("Maximum number of sticks? ")

            # Create initial state
            for i in range(int(numPiles)):
                # Use random numbers to generate random number of sticks
                sticks = random.randint(1,int(maxSticks))
                initialState.append(sticks)

            # set first or second go and create state
            print("The intial state is " + str(initialState))
            print("Do you want to play a) first or b) second")
            turn = input("Enter a or b")
            if(str(turn).lower() ==  "a"):
                state = (initialState,1) #user is always MAX player
                valid = True

            elif(str(turn).lower() == "b"):
                state = (initialState,2) #AI is always MIN player
                valid = True

            else:
                raise ValueError("Invalid Input")
        except ValueError:
            print("invalid input, please re-enter")

    # Return state so we can start game
    return state

# Given a state, start the game
def game_begin(state):

    game_state = state

    print("game start ", game_state)
    # while no winner, keep alternating
    while game_state[0] != []:


        if(game_state[1]==1):
            # game_state = user_turn(game_state)
            game_state = AI_player_mcts(game_state)
        else:
            game_state = AI_player_mcts(game_state)
       # print("state is", game_state)

    # if final state is 1, 2 wins
    if(game_state[1] == 2):
        print("win for teh computer")
    else:
        print("You win!")

# The user turn, let them choose
def user_turn(state):
    # Get states
    succ = successors(state)

    # if only an empty state left, pick the stick and return
    if(len(succ)==1):
        print("Only one stick left, and you picked it up")
        return succ[0]
    # Print list of moves
    print("Next move options:")
    for i in range(len(succ)):
        print(str(i) + ".    " + str(succ[i][0]))
    moveIndex = input("Enter next move option number ")
    print("You moved to state " + str(succ[int(moveIndex)][0]))

    # Set new state and return
    state = succ[int(moveIndex)]
    return state

def test_timing(state):
    # Start a timer
    start = time.time()
    # Call minimax function
    #value = minimax_value(state)
    value = AI_player_mcts(state)
    end = time.time()
    #calculate and return
    duration = end-start
    #print('Time taken:', duration)
    return duration, value


# A very basic AI, uses pruned minimax
def AI_player_mcts(state):

    game_state = MCTS(state)

    print("")
    print("AI player moved to state " + str(game_state))
    return game_state

init_state = ([20,20,20,20,20],1)
game_begin(init_state)

