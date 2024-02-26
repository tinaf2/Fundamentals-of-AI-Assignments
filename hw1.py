##############
# Homework 2 #
##############

##############
# Question 1 #
##############

"""
Performs a breadth-first search on a tree represented by nested tuples
Arguments:
    FRINGE: A tuple representing the root of the search tree
Returns:
    tuple: A tuple containing the leaf nodes of the tree, in the order they are visited by left-to-right BFS
"""
def BFS(FRINGE):

    queue = list(FRINGE)   # initialize queue with input nodes
    
    result = [] # initialize list to store the result

    while queue:
        current = queue.pop(0)         # get the first element from the queue

        if isinstance(current, tuple):
            queue.extend(current) # if current element is a tuple, add its children to the queue for processing
        else:
            result.append(current)   # if current element is a leaf node, add it to the result list

    return tuple(result)

# test cases
print(BFS(("ROOT",)))  # ('ROOT',)
print(BFS((((("L", "E"), "F"), "T"))))  # ('T', 'F', 'L', 'E')
print(BFS((("R", ("I", ("G", ("H", "T")))))))  # ('R', 'I', 'G', 'H', 'T')
print(BFS(((("A", ("B",)), "C", ("D",)))))  # ('C', 'A', 'D', 'B')
print(BFS((("T", ("H", "R", "E"), "E"))))  # ('T', 'E', 'H', 'R', 'E')
print(BFS((("A", (("C", (("E",), "D")), "B")))))  # ('A', 'B', 'C', 'D', 'E')



##############
# Question 2 #
##############


# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS returns [].
# To call DFS to solve the original problem, one would call
# DFS((False, False, False, False), [])
# However, it should be possible to call DFS with a different initial
# state or with an initial path.

# First, we define the helper functions of DFS.

# FINAL-STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
"""
Checks if the current state is the goal state.
Arguments:
     S: A tuple representing the current state (homer, baby, dog, poison).
Returns: 
    True if the current state is the goal state, False otherwise.
"""
def FINAL_STATE(S):
    return S == (True, True, True, True)


# NEXT-STATE returns the state that results from applying an operator to the
# current state. It takes three arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns None.
# NOTE that next-state returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
"""
Compute the next state based on the current state and action.
Arguments:
    S: A tuple representing the current state
    A: A string representing the action (either 'h', 'b', 'd', or 'p')
Returns: 
    A list containing the successor state as a tuple, or None if the state is invalid
"""
def NEXT_STATE(S, A):
    homer, baby, dog, poison = S
    if A == 'b' and homer != baby: # cant move homer/baby if they are not on same side
        return None
    elif A == 'd' and homer != dog: # cant move homer/dog if they are not on same side
        return None
    elif A == 'p' and homer != poison: # cant move homer/poison if they are not on same side
        return None
    # initial check for bad move
    elif A == 'h' and homer == baby and homer == dog: # if homer leaving baby unattended with dog
        return None
    elif A == 'h' and homer == baby and homer == poison: # if homer leaving baby unattended with poison
        return None
    elif A == 'd' and baby == poison: # if homer/dog leaving baby/poison unattended
        return None
    elif A == 'p' and baby == dog: # if homer/poison leaving baby/dog unattended
        return None
    

    
    next_state = list(S) # initialize list representing new state
    next_state[0] = not next_state[0] # homer is moving regardless
    next_state[1] = baby
    next_state[2] = dog
    next_state[3] = poison

    if A != 'h':
        index = {'b': 1, 'd': 2, 'p': 3}[A]
        next_state[index] = not next_state[index] # change index of any other thing moved with homer

    if (next_state[1] == next_state[2] and next_state[0] != next_state[1]) or \
       (next_state[1] == next_state[3] and next_state[0] != next_state[1]):
        return None # double check that baby/dog or baby/poison have not been left unattended without homer
    return [tuple(next_state)]



# SUCC-FN returns all of the possible legal successor states to the current
# state. It takes a single argument (s), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
"""
Generate all successor states from the current state
Arguments:
    S: A tuple representing the current state
Returns: 
    successors: A list of all valid successor states
"""
def SUCC_FN(S):
    successors = []
    for move in ['h', 'b', 'd', 'p']:
        next_state = NEXT_STATE(S, move) # try each possible move/operator on this state
        if next_state:
            successors.extend(next_state) # if that move produces valid state, add state to list of successors
    return successors



# ON-PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if s is a member of
# states and False otherwise.
"""
Check if a state is already on the path visited by this DFS
Arguments:
    S: The current state to check.
    STATES: A list of states representing the path
Returns: 
    True if S is in STATES, False otherwise
"""
def ON_PATH(S, STATES):
    return S in STATES


# MULT-DFS is a helper function for DFS. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT-DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT-DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].
"""
Perform DFS on each state in STATES.
Arguments:
    STATES: A list of states to perform DFS on.
    PATH: The current path of states.
Returns: 
    The path to the goal state, or [] if no such path.
"""

def MULT_DFS(STATES, PATH):
    if not STATES: # base case: if there are no states to explore, return None
        return None
    first_state = STATES[0]
    if FINAL_STATE(first_state): # check if the first state is a final state
        return PATH + [first_state] 
    if first_state in PATH: # if we have encountered a cycle
        return MULT_DFS(STATES[1:], PATH) # skip this state and continue with rest
    res = MULT_DFS(SUCC_FN(first_state), PATH + [first_state]) # explore the successors of the first state recursively, adding the first state to the path
    if res: 
        return res # if a solution is found in the subtree of this state, return the result
    else:
        return MULT_DFS(STATES[1:], PATH) # if no solution is found, backtrack and continue with the next state in the STATES list


# DFS does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to False. DFS
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or False otherwise. DFS is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path.
"""
Perform a depth-first search from a given state to the goal state.
Arguments:
    S: The current state.
    PATH: The path of states leading to S.
Returns: 
    The path from the initial state to the goal state, or [] if no such path.
"""

def DFS(S, PATH):
    if ON_PATH(S, PATH): # check if nnode has already been visited
        return None
    
    if FINAL_STATE(S): # check for goal state
        return PATH + [S]

    return MULT_DFS(SUCC_FN(S), PATH + [S]) # perform DFS on every successor state starting from the start state
    

# test cases

# solve the problem starting from initial state where everyone is on the west side
solution_path = DFS((False, False, False, False), [])
print("Solution Path:", solution_path)


def test_final_state():
    assert FINAL_STATE((True, True, True, True)) == True, "Test failed: Goal state should return True"
    assert FINAL_STATE((False, True, True, True)) == False, "Test failed: Non-goal state should return False"
    assert FINAL_STATE((True, False, True, True)) == False, "Test failed: Non-goal state should return False"

test_final_state()

def test_next_state():
    # Test moving Homer and baby when they are on the same side
    assert NEXT_STATE((True, True, False, False), 'b') == [(False, False, False, False)], "Test failed: Moving Homer and baby"

    # Test moving Homer alone back to the other side
    assert NEXT_STATE((False, False, False, False), 'h') == None, "Test failed: Homer should not leave everyone else alone"

    # Test invalid move: Homer tries to move with the dog while not on the same side
    assert NEXT_STATE((True, True, False, False), 'd') == None, "Test failed: Invalid move with dog"

    # Test invalid move: Leaving baby alone with poison
    assert NEXT_STATE((True, True, True, True), 'h') == None, "Test failed: Invalid move leaving baby with poison"

test_next_state()

def test_succ_fn():
    # Test successor function from a valid state
    assert set(SUCC_FN((False, False, True, True))) == set([(True, False, True, True), (True, True, True, True)]), "Test failed: Successor function from valid state"

    # Test successor function from another valid state
    assert set(SUCC_FN((True, False, True, True))) == set([(False, False, True, True), (False, False, False, True),
                                                            (False, False, True, False)]), "Test failed: Successor function from another valid state"

test_succ_fn()

def test_on_path():
    # Test if a state is on the path
    assert ON_PATH((True, True, True, True), [(False, False, False, False), (True, True, True, True)]) == True, "Test failed: State should be on path"

    # Test if a state is not on the path
    assert ON_PATH((True, False, True, True), [(False, False, False, False), (True, True, True, True)]) == False, "Test failed: State should not be on path"

# Run the tests
test_on_path()


