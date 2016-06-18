__author__ = 'yusuf'
from copy import deepcopy


###################################
#                 -------------   #
#                 | 1 | 2 | 3 |   #
#                 -------------   #
#   GOAL STATE:   | 4 | 5 | 6 |   #
#                 -------------   #
#                 | 7 | 8 |   |   #
#                 -------------   #
###################################

# 0 means black tile
goal_state = [[1,2,3],[4,5,6],[7,8,0]]
initial_state = [[1,0,3],[4,2,5],[7,8,6]]

# convert_to_1D Function
# Takes two dimensional array -> Return one dimensional array
# Purpose -> Returns the list form of the given matrix for convenience

def convert_to_1D(matrix_2D):
    matrix_1D = list()
    for row in range(len(matrix_2D)):
        for col in range(len(matrix_2D)):
            matrix_1D.append(matrix_2D[row][col])
    return matrix_1D

# num_of_inversion Function
# Takes an array -> Return a number
# Purpose -> Returns the total number of inversions in the matrix (not taking the blank tile into account)

def num_of_inversion(matrix_1D):
    inversion = 0
    for index in range(len(matrix_1D)):
        tmp = matrix_1D [index]
        if tmp == 0 or tmp == 1:
            continue
        for elem in matrix_1D[index:]:
            if elem == 0:
                continue
            if tmp > elem:
                inversion +=1
    return inversion


# is_valid Function
# Takes two dimensional array -> Returns boolean
# Purpose -> Checks whether the given matrix is valid or not,
# i.e., having 9 integers from 0 to 8 with no repetition,

def is_valid(matrix):
    sum_of_numbers = 0
    sum_of_squares = 0
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            sum_of_numbers += matrix[row][col]
            sum_of_squares += pow(matrix[row][col],2)
    if sum_of_numbers == 36 and sum_of_squares == 204:
        return True
    else:
        return False

###################################

# Alternatively

def is_valid2(matrix):
    initial_list = convert_to_1D(matrix)
    validity = bool()
    if len(initial_list) is not 9:
        return validity # False
    check = int()
    goal_list = convert_to_1D(goal_state)
    for number in goal_list:
        if number in initial_list:
            check += 1
    if check is 9:
        return not validity # True
    else:
        return validity # False

##################################

# is_solvable Function
# Takes array as input -> Returns boolean
# Purpose -> Checks whether the matrix is solvable or not
# according to the goal state and returns true
# if it is solvable, or false, otherwise.

def is_solvable(matrix):
    if not is_valid(matrix):
        print("Error, Matrix is not valid")
    else:
        goal = num_of_inversion(goal_state) # inversion of goal state
        inital = num_of_inversion(matrix)   # inversion of initial state
        if (goal % 2) == 0 and (inital % 2) == 0:
            return True
        elif (goal % 2) == 1 and (inital % 2) == 1:
            return True
        else:
            return False

# find_row_col Function
# Takes a matrix and a int value -> Returns tuple
# Purpose -> Returns a tuple consisting of row and column
# of the given value in the matrix.

def find_row_col(matrix,value):
    if value < 0 or value > 8:
        raise Exception ("Give the value is out of range")
    else:
        for row in range(len(matrix)):
            for col in range(len(matrix)):
                if (matrix[row][col] == value):
                    return row, col

# possible_moves Function
# Takes a matrix as input -> Return list of tuple
# Purpose -> Find possible positions of blank tile can move

def possible_moves(matrix):
    row,col = find_row_col(matrix,0)
    possible_moves = list()
    if row > 0:
                possible_moves.append((row-1,col))
    if row < 2:
                possible_moves.append((row+1,col))
    if col > 0:
                possible_moves.append((row,col-1))
    if col < 2:
                possible_moves.append((row,col+1))
    return possible_moves

# get_value and set_value Functions
# Helper functions for swap_blank_tile

def get_value(matrix,row,col):
    return matrix[row][col]

def set_value(matrix,row,col,value):
    matrix[row][col] = value

# swap_blank_tile Function
# Takes a matrix and a tuple -> Returns a tuple
# Purpose -> Swaping the blank tile

def swap_blank_tile(matrix,next_pos):
    row,col = find_row_col(matrix,0)
    next_pos_row = next_pos[0]
    next_pos_col = next_pos[1]
    blank_tile = get_value(matrix,row,col)
    next_tile = get_value(matrix,next_pos_row,next_pos_col)
    set_value(matrix,row,col,next_tile)
    set_value(matrix,next_pos_row,next_pos_col,blank_tile)
    return  matrix

#print(swap_blank_tile(initial_state,(0,2)))

# hamming_distance Function
# Takes a matrix -> Return an integer
# Purpose -> Finding number of tiles in wrong position

def hamming_distance(matrix):
    starting_matrix = convert_to_1D(matrix)
    result_matrix = convert_to_1D(goal_state)
    tmp = 0
    for i in range(0,9):
        if((starting_matrix[i] != result_matrix[i]) & (starting_matrix[i] != 0)):
            tmp+=1
    return tmp

# manhattan_distance Function
# Takes a matrix -> Return an integer
# Purpose -> Finding sum of the distances
# (sum of the horizontal and vertical distances)
# of the tiles from their goal positions

def manhattan_distance(matrix):
    tmp = 0
    for i in range(1,9):
        row,col = find_row_col(matrix,i)
        row2,col2 = find_row_col(goal_state,i)
        a = row+col
        b = row2+col2
        tmp += abs(a-b)
    return tmp


# Best-first-search Funtion
# Takes a matrix -> shows possible steps for solution
# Purpose -> Reach the goal state from given matrix

def bfs(matrix):
    #List of possible matrix
    possible_matrix = list()
    hamming_list = list()
    chosen_matrix = matrix
    for i in possible_moves(matrix):
        matrix2 = deepcopy(matrix)
        b = swap_blank_tile(matrix2,i)
        possible_matrix.append(b)
    for j in range(len(possible_matrix)):
        c = hamming_distance(possible_matrix[j])
        hamming_list.append(c)
    for k in range(len(possible_matrix)):
        if(hamming_list[k] == min(hamming_list)):
            chosen_matrix = possible_matrix[k]
    #print(possible_matrix)
    #print(hamming_list)
    print(chosen_matrix)
    if chosen_matrix == goal_state:
        print("REACHED THE GOAL STATE")
    else:
        bfs(chosen_matrix)

#######################################
# Simple matrix can be solve, but
# complex matrix causes infinite loop
# so bfs function need to be modify
#######################################

test1 = [[1,2,3],[4,5,6],[0,7,8]] # 2 STEP
test2 = [[1,2,3],[0,4,5],[7,8,6]] # 3 STEP

# After 3. step, all possible matrix have same hamming distance
# So it goes infinite loop
test3 = [[0,2,3],[1,4,6],[7,8,5]]

bfs(test1)
bfs(test2)
#bfs(test3) -> Causes Infinite loop