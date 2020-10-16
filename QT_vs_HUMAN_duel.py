# TNM108 - Lab 0 by Nichoals Frederiksen/nicfr426

import numpy as np
import math
import os
import time
from datetime import datetime
import h5py
import copy
import random
import pickle

def get_empty_board():
    board = []
    for i in range(3):
        board.append([[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]])
    return board

def is_board_empty(board):
    # check is board is empty, no pieces.
    for row in range(3):
        for col in range(3):
            if board[0][row][col] != " ":
                return False
    return True

def is_board_full(board):
    for row in range(3):
        for col in range(3):
            if board[0][row][col] == " ":
                return False
    return True

def only_one_empty(board):
    counter = 0
    for row in range(3):
        for col in range(3):
            if board[0][row][col] == " ":
                counter += 1
    if counter == 1:
        return True
    else:
        return False

def is_tie(board):
    tie = True
    for row in range(3):
        for col in range(3):
            if board[0][row][col] == " ":
                tie = False
                return tie
    return tie

def is_gameover(board, win):
    pos_mov = np.array(possiblePos(board))
    if pos_mov.size == 0:
        return True
    if win:
        return True
    return False

def empty_trapboard(board):
    temp = ([[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]])
    board[1] = temp
    return board

def print_board(totalBoard):
    firstRow = ""
    secondRow = ""
    thirdRow = ""
    # To only view YOUR traps
    totalBoard = totalBoard[:2]
    # Takes each board, saves the rows in a variable, then prints the variables
    for b in range(len(totalBoard)):
        firstRow = firstRow + "|" + " ".join(totalBoard[b][0]) + "|"
        secondRow = secondRow + "|" + " ".join(totalBoard[b][1]) + "|"
        thirdRow = thirdRow + "|" + " ".join(totalBoard[b][2]) + "|"

        # if 3 boards have been collected, then it prints the boards out
        # and resets the variables (firstRow, secondRow, etc.)

    print("-------")
    print(firstRow)
    print("-------")
    print(secondRow)
    print("-------")
    print(thirdRow)

def possiblePos(board):
# FUNCTION OUTPUTS A LIST
    # Amount of columns in the Q-table.
    QT_XSIZE = 72
    # If board is empty then all columns in the table are valid.
    if is_board_empty(board):
        return range(QT_XSIZE)

    possibleIndex = []
    possibleCombos = []

    # otherwise, finds all available spaces in the subBoard

    for row in range(3):
        for coloumn in range(3):
            if board[0][row][coloumn] == " " and board[1][row][coloumn] == " ":
                poss_ph1_act = (row * 3) + coloumn
                for r in range(3):
                    for c in range(3):
                        if board[0][r][c] == " " and ((r * 3) + c) != poss_ph1_act:
                            poss_ph2_act = (r * 3) + c
                            temp = np.array([poss_ph1_act, poss_ph2_act])
                            possibleCombos.append(temp)

    ALL_MOVES = all_moves(QT_XSIZE)
    pc = np.array(possibleCombos)
    for j in range(len(pc)):
        for i in range(len(ALL_MOVES)):
            if ALL_MOVES[i][0] == pc[j][0] and ALL_MOVES[i][1] == pc[j][1]:
                possibleIndex.append(i)

# IN CASE RULE 4 IS ENFORCED - rules for possible moves are different,
# possibleIndex will be = [] in that case.
    if not possibleIndex:
        if only_one_empty(board):
            for row in range(3):
                for coloumn in range(3):
                    if board[0][row][coloumn] == " " and board[1][row][coloumn] == " ":
                        poss_ph1_act = (row * 3) + coloumn
                        arr = np.arange(9)
                        arr = np.delete(arr, poss_ph1_act)
                        arr2 = random.choice(arr)
                        poss_ph2_act = arr2
                        temp = np.array([poss_ph1_act, poss_ph2_act])
                        possibleCombos.append(temp)

            ALL_MOVES = all_moves(QT_XSIZE)
            pc = np.array(possibleCombos)
            for j in range(len(pc)):
                for i in range(len(ALL_MOVES)):
                    if ALL_MOVES[i][0] == pc[j][0] and ALL_MOVES[i][1] == pc[j][1]:
                        possibleIndex.append(i)

    if len(possibleIndex) > 0:
        return possibleIndex


    return possibleIndex

def possiblePos2Kill(board, player):

    possible = []
    remove_an = ""

    # Figure out which pieces we are allowed to remove/kill
    if player == -1:
        remove_an = 'O'
    if player == 1:
        remove_an = "X"

    for row in range(3):
        for coloumn in range(3):
            if board[0][row][coloumn] == remove_an:
                possible.append((row * 3) + coloumn)

    if len(possible) > 0:
        return possible

    return possible

def swapBoard_me_and_her(board):
    temp = board[2]
    board[2] = board[1]
    board[1] = temp
    return board

def move_phase1(board, action, player):
    if player == 1:
        turn = 'X'
    if player == -1:
        turn = "O"

    action_int = int(action)

    bestPosition = []
    new_board = copy.deepcopy(board)
    # To convert action [int range 0-8] to board coordinates row=0:2, col=0:2
    remainder = action_int % 9
    bestPosition.append(int(remainder / 3))
    bestPosition.append(remainder % 3)

    # place piece at position on board
    new_board[0][bestPosition[0]][bestPosition[1]] = turn

    wonBoard = False
    win = False
    x = bestPosition[0]
    y = bestPosition[1]

    # check for win on verticle
    if new_board[0][0][y] == new_board[0][1][y] == new_board[0][2][y]:
        # print("yahoo! on the verticle")
        wonBoard = True

    # check for win on horozontal
    if new_board[0][x][0] == new_board[0][x][1] == new_board[0][x][2]:
        # print("yahoo! on the horizontal")
        wonBoard = True

    # check for win on negative diagonal
    if x == y and new_board[0][0][0] == new_board[0][1][1] == new_board[0][2][2]:
        # print("yahoo! on the backslash")
        wonBoard = True

    # check for win on positive diagonal
    if x + y == 2 and new_board[0][0][2] == new_board[0][1][1] == new_board[0][2][0]:
        # print("yahoo! on the forwardslash")
        wonBoard = True


    if wonBoard == True:
        win = True

    return new_board, win # out: board

# Decide for Phase 2 or Phase 3 + Phase 2.5
def trigger_test(new_board):
    # new_board[0] -> is the gameboard
    # new_board[2] -> is the enemy's trapboard
    for row in range(3):
        for col in range(3):
            # Check for a Pos where a marker is on both boards.
            if new_board[0][row][col] != " " and new_board[2][row][col] == "T":
                print("**TRAP TRIGGERED!** b[0]:"+ new_board[0][row][col] + " b[2]:"+ new_board[2][row][col])
                return True
    return False

def move_phase2(boardreal, action):
    board = copy.deepcopy(boardreal)
    # Clear the TRIGGER/TRAP board
    board[1] = [[" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]]
    bestPosition = []
    action_int = int(action)
    # To convert action [int range 0-8] to board coordinates row=0:2, col=0:2
    remainder = action_int % 9
    bestPosition.append(int(remainder / 3))
    bestPosition.append(remainder % 3)

    # place piece at position on board
    board[1][bestPosition[0]][bestPosition[1]] = "T"

    return board

# TRAP-PHASE
def move_phase3(boardreal, action):
    board = copy.deepcopy(boardreal)
    bestPosition = []
    action_int = int(action)
    # To convert action [int range 0-8] to board coordinates row=0:2, col=0:2
    remainder = action_int % 9
    bestPosition.append(int(remainder / 3))
    bestPosition.append(remainder % 3)

    # place an empty piece at position on board
    enemy_XorO = board[0][bestPosition[0]][bestPosition[1]]

    board[0][bestPosition[0]][bestPosition[1]] = " "

    wonBoard = False
    win = False
    x = bestPosition[0]
    y = bestPosition[1]

    # check for win on negative diagonal \
    if board[0][0][0] == enemy_XorO and board[0][1][1] == board[0][0][0] == board[0][2][2]:
        wonBoard = True

    # check for win on positive diagonal /
    if  board[0][0][2] == enemy_XorO and board[0][0][2] == board[0][1][1] == board[0][2][0]:
        wonBoard = True

    # Check hori. win for selected row. --
    for row in range(3):
        if board[0][row][0] == enemy_XorO and board[0][row][0] == board[0][row][1] == board[0][row][2]:
            wonBoard = True

    # Check vert. win for selected col. |
    for col in range(3):
        if board[0][0][col] == enemy_XorO and board[0][0][col] == board[0][1][col] == board[0][2][col]:
            wonBoard = True

    # if the subBoard was won, checking whether the entire board is won as well
    if wonBoard == True:
        win = True

    return board, win

# output same as action
def human_turn(board, turn):
    print_board(board)
    print("It is " + turn + "'s turn")

    while True:
        try:
            y = int(input("Please enter y coordinate")) - 1
            x = int(input("Please enter x coordinate")) - 1
        except ValueError:
            print("One of those inputs were not valid integers, please try again")
            continue
        if y not in range(3) or x not in range(3):
            print("Integers must be between 1 and 3, please try again")
            continue
        if board[0][y][x] != " ":
            print("That space has already been taken, please try again")
            continue
        if board[1][y][x] != " ":
            print("That space has a cool-down, please try another")
            continue
        else:
            return y * 3 + x

def human_turn_kill(board, turn):
    print_board(board)
    print("It is " + turn + "'s turn")

    if turn == "O":
        remove_a = "X"
    if turn == "X":
        remove_a = "O"


    while True:
        try:
            y = int(input("Please enter y coordinate")) - 1
            x = int(input("Please enter x coordinate")) - 1
        except ValueError:
            print("One of those inputs were not valid integers, please try again")
            continue
        if y not in range(3) or x not in range(3):
            print("Integers must be between 1 and 3, please try again")
            continue
        if board[0][y][x] != remove_a:
            print("That space cannot be removed, please try again")
            continue
        else:
            return y * 3 + x

def letter_to_int(letter, player):
    # based on the letter in a box in the board, replaces 'X' with 1 and 'O' with -1
    if letter == 'v':
        return 0
    elif letter == " ":
        return 0
    elif letter == "X":
        return 1 * player
    elif letter == "O":
        return -1 * player

def board_to_array(boardreal, player):
    # makes copy of board, so that the original board does not get changed
    board = copy.deepcopy(boardreal)

    # takes a board in its normal state, and returns a 9x9 numpy array, changing 'X' = 1 and 'O' = -1
    # also places a 0.1 in all valid board positions

    # board = fill_winning_boards(board)
    tie = True

    # if it is the first turn, then all of the cells are valid moves
    if is_board_empty(board):
        return np.full((3, 3), 0)

    # replacing all valid positions with 'v'
    # checking whether all empty values on the board are valid

    for line in range(3):
        for item in range(3):
            if board[0][line][item] == " ":
                board[0][line][item] = 'v'
                tie = False

    # if the miniboard ends up being a tie
    if tie:
        for line in range(3):
            for item in range(3):
                if board[0][line][item] == " ":
                    board[0][line][item] = 'v'

    array = []
    firstline = []
    secondline = []
    thirdline = []



    for item in board[0][0]:
        firstline.append(letter_to_int(item, player))

    for item in board[0][1]:
        secondline.append(letter_to_int(item, player))

    for item in board[0][2]:
        thirdline.append(letter_to_int(item, player))


    array.append(firstline)
    array.append(secondline)
    array.append(thirdline)


    board_array = np.array(array)

    return board_array

#Returns best Q-table action-index for state.
def best_action_from_table(STATE, QTABLE):

    possibles_moves = np.array(possiblePos(STATE))
    # Out of poss moves find the highest value
    max_value = np.max(QTABLE[str(STATE[:2])][possibles_moves])
    # Find index of max value amongst all moves.
    the_actions = np.where(QTABLE[str(STATE[:2])] == max_value)
    # In case that there is a tie (multiple indices), then randomly select one.
    while True:
        action_bad_format = np.random.choice(the_actions[0], 1)
        BEST_ACT = action_bad_format[0]
        if BEST_ACT in possibles_moves:
            break
    return BEST_ACT

def table_index_to_actioncombo(value):
    QT_XSIZE = 72
    ALL_MOVES = all_moves(QT_XSIZE)

    ph1_action_and_ph2_action = ALL_MOVES[value]

    return ph1_action_and_ph2_action

def actioncombo_to_table_index(combo_arr):
    # Given an array([2,4])
    QT_XSIZE = 72
    ALL_MOVES = all_moves(QT_XSIZE)

    for i in range(len(ALL_MOVES)):
        if combo_arr[0] == ALL_MOVES[i][0] and combo_arr[1] == ALL_MOVES[i][1]:
            return i

def all_moves(col):

    bad = np.zeros((1, col, 2))
    ALL_MOVES = bad[0]

    for first in range(9):
        for second in range(8):
            trap_coords = np.arange(9)
            ALL_MOVES[second + first * 8][0] = first

            trap_coords = np.delete(trap_coords, first)
            ALL_MOVES[second + first * 8][1] = trap_coords[second]

    return ALL_MOVES

def print_row_nice(state, QT):
    str_state = str(state[:2])
    ugly_row = QT[str_state]
    print_this = []
    for idx in range(72):
        print_this.append(ugly_row[idx])
        if idx > 1 and len(print_this) % 8 == 0:
            print("variants of ACTION:" + str((int((idx + 1) / 8)) - 1), print_this)
            print_this = []

def playgame_dude_vs_dude():
    board = get_empty_board()

    while True:
        #________________________
        # ____X's turn!____
        #________________________

        # Trap info Swappage
        board = swapBoard_me_and_her(board)

        # PHASE 1 - Place a soldier!
        print("\n \n PLACE A SOLDIER!")
        action_phase1 = human_turn(board, 'X')
        print("action phase1:" + str(action_phase1))
        next_board, wonBoard = move_phase1(board, action_phase1, 1)

        if trigger_test(next_board):
            # Should be O's turn now
            print("\n \n REMOVE ANY 'X'")
            action_phase3 = human_turn_kill(board, 'O')
            print("action phase3:" + str(action_phase3))
            next_board, wonBoard = move_phase3(board, action_phase3)
            # FOR IF HE FAILED TO REMoVE a Win-contributing piece
            if wonBoard:
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            else:
                board = next_board


            # PHASE 2.5 - Lay a trap! Back to X's turn
            print("\n \n TIME TO LAY A TRAP! ;-)")
            board = empty_trapboard(board)
            action_phase2 = human_turn(board, 'X')
            print("action phase2.5:" + str(action_phase2))
            next_board = move_phase2(board, action_phase2)

            # Update again before kicking it to the next player
            board = next_board
        else:
            if wonBoard:
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            elif is_tie(next_board):
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("IT'S A DRAW / TIE")

                break
            else:
                board = next_board

            if only_one_empty(board):
                # Clear the TRIGGER/TRAP boards
                board[2] = board[1] = [[" ", " ", " "],
                            [" ", " ", " "],
                            [" ", " ", " "]]
                # And skip Phase 2
            else:
                # PHASE 2 - Lay a trap!
                print("\n \n TIME TO LAY A TRAP! ;-)")
                board = empty_trapboard(board)
                action_phase2 = human_turn(board, 'X')
                print("action phase2:" + str(action_phase2))
                next_board = move_phase2(board, action_phase2)

                # Update again before kicking it to the next player
                board = next_board

        #________________________
        # ____O's turn!____
        #________________________

        # Trap info Swappage
        board = swapBoard_me_and_her(board)

        # PHASE 1 - Place a soldier!
        print("\n \n PLACE A SOLDIER!")
        action_phase1 = human_turn(board, 'O')
        print("action phase1:" + str(action_phase1))
        next_board, wonBoard = move_phase1(board, action_phase1, -1)

        if trigger_test(next_board):
            # Should be X's turn now
            print("\n \n REMOVE ANY 'O'")
            action_phase3 = human_turn_kill(board, 'X')
            print("action phase3:" + str(action_phase3))
            next_board, wonBoard = move_phase3(board, action_phase3)

            if wonBoard:
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            else:
                board = next_board

            # PHASE 2.5 - Lay a trap! Back to O's turn
            print("\n \n TIME TO LAY A TRAP! ;-)")
            board = empty_trapboard(board)
            action_phase2 = human_turn(board, 'O')
            print("action phase2:" + str(action_phase2))
            next_board = move_phase2(board, action_phase2)

            # Update again before kicking it to the next player
            board = next_board
        else:
            if wonBoard:
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            elif is_tie(next_board):
                print("________________ \(^___^)/ ")
                print_board(next_board)
                print("_________________ \(O _ -) ")
                print("IT'S A DRAW / TIE")

                break
            else:
                board = next_board

            if only_one_empty(board):
                # Clear the TRIGGER/TRAP boards
                board[2] = board[1] = [[" ", " ", " "],
                                       [" ", " ", " "],
                                       [" ", " ", " "]]
                # And skip Phase 2
            else:
                # PHASE 2 - Lay a trap!
                print("\n \n TIME TO LAY A TRAP! ;-)")
                board = empty_trapboard(board)
                action_phase2 = human_turn(board, 'O')
                print("action phase2:" + str(action_phase2))
                next_board = move_phase2(board, action_phase2)

                # Update again before kicking it to the next player
                board = next_board

#---------------------------------------------------------------Q TABLE STUFF--------------------------------


qtable = {}

#filename = 'v2Q_TABLE_4_QTvHE_35k.pickle'
#filename = 'Q_TABLE_4_QTvHE_50k.pickle'
#filename = 'Q_TABLE_4_QTvQT_100k.pickle'   # BAD
#filename = 'Q_TABLE_4_QTvQT_150k.pickle'   # BAD
#filename = 'Q_TABLE_4_QTvRA_10k.pickle'     # BAD
#filename = 'v2Q_TABLE_4_QTvQT_10k.pickle'     # Won once. but bad
#filename = 'v3Q_TABLE_4_QTvHE_30kC.pickle'
#filename = 'v3Q_TABLE_4_QTvHE_20kC.pickle'      # NOW its the golden god!? WTF==?? 100%
#filename = 'the_golden_god_20kC.pickle'
#filename = '1__deleteme.pickle'
filename = 'GOOD_TABLE_DEMO.pickle'


# LOAD Q TABLE
with open(filename, 'rb') as handle:
    qtable = pickle.load(handle)


# List of rewards
WIN_REWARD = 1
TIE_REWARD = 0.5
HIT_REWARD = 0.25
MISS_REWARD = -0.15
LOSE_REWARD = -1

learning_rate = 0.3         # Learning rate
gamma = 1                 # Discounting rate

# Exploration parameters
epsilon = 0.0001                # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.0001            # Minimum exploration probability
decay_rate = 0.005            # Exponential decay rate for exploration prob

def playgame():

    state = get_empty_board()
    current_player = 1  # start a X
    xsize = 72
    opp_state = ""
    opp_action = 0


# _______________________________________________________________________________________*
# ----- THE GAMES BEGIN! ----------------------------------------------------------------*
# _________________________________________ROBOT'S TURN__________________________________*
    while True:

        # New state for current player.
        str_state = str(state[:2])
        # New reset action index for current player.
        action_index = 0

        ## IF IT'S NEW TO THE TABLE
        if str_state not in qtable:
            # Add the Board to the dict w/ value = empty 1x9 array
            qtable[str_state] = np.zeros(xsize)

        ## If this number > greater than epsilon --> Use table. Else RANDOM.
        exp_exp_tradeoff = random.uniform(0, 1)
        if exp_exp_tradeoff > epsilon:
            # So... action_index = table_value basically
            action_index = best_action_from_table(state, qtable)
            LOG_ACTION = table_index_to_actioncombo(action_index)
            # LOG_ACTION = array([0, 1]) 4 example. Meaning place soldier at 0 and trap at 1.
            action_phase1 = LOG_ACTION[0]
            LOG_CHOICE = "-TABLE-"
        # Else doing a random choice --> exploration
        else:
            action_index = random.choice(possiblePos(state))
            LOG_ACTION = table_index_to_actioncombo(action_index)
            action_phase1 = LOG_ACTION[0]
            LOG_CHOICE = "-RANDOM-"



        # **************** ** NEW STATE ** PHASE 1 COMPLETE ** ***********AI
        new_state, win = move_phase1(state, action_phase1, current_player)
        # ****************************************************************
        print("QTABLE ROWS--")
        print_row_nice(state, qtable)
        print("ROBOT chose with " + LOG_CHOICE)
        print("PLAYER-X PLACED A SOLDIER")
        print("new_state:")
        print_board(new_state)
        # Before trigger-test, check if state is already in tie state. if yes, yeet!
        if is_board_full(new_state):
            if win:
                print(
                    "-----------------------------------------------------------break#-1 --- GAME ENDS IN AUTO-WIN ---")
                qtable[str(state[:2])][action_index] = WIN_REWARD
                break
            if is_tie(new_state):
                print(
                    "-----------------------------------------------------------------------break#0 --- GAME ENDS IN TIE")
                qtable[str(state[:2])][action_index] = TIE_REWARD
                break





        # ***________TRIGGER TEST!____________***
        if trigger_test(new_state):
            print("**TRAP TRIGGERED**")
            qtable[opp_state][opp_action] = HIT_REWARD
            # Should be O's turn now
            print("\n \n REMOVE ANY 'X'")
            action_phase3 = human_turn_kill(new_state, 'O')
            print("action phase3:" + str(action_phase3))
            # ****************** PHASE 3 COMPLETE ****************************HU
            next_next_state, wonBoard = move_phase3(new_state, action_phase3)
            # ****************************************************************
            # FOR IF HE FAILED TO REMoVE a Win-contributing piece
            if wonBoard:
                print("----------------------------------------------------------------------break#1 [cuz fail kill]")
                print_board(next_next_state)
                break
            else:
                new_state = next_next_state
                win = wonBoard
                print("state minus a soldier")
                print_board(new_state)

            # PHASE 2.5 - Lay a trap! Back to X's turn
            # __________- AI can't learn from this part.
            str_state = str(new_state[:2])
            if str_state not in qtable:
                qtable[str_state] = np.zeros(xsize)

            exp_exp_tradeoff = random.uniform(0, 1)  # Look at Table or Random.
            if exp_exp_tradeoff > 0.5:
                # IN PLACE OF THE FALLEN SOLDIER
                action_phase2 = action_phase3
            # Else doing a random choice --> exploration
            else:
                index = random.choice(possiblePos(new_state))
                LOG_ACTION_2 = table_index_to_actioncombo(index)
                LOG_ACTION[1] = LOG_ACTION_2[1]
                action_index = actioncombo_to_table_index(LOG_ACTION)
                action_phase2 = LOG_ACTION[1]

            # ***************** PHASE 2.5 COMPLETE  **************************AI
            next_state = move_phase2(new_state, action_phase2)
            # ****************************************************************
            # Update again before kicking it to the next player
            state = next_state
            state = swapBoard_me_and_her(state)
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**
            print("After phase3. Time for Player-X to lay his trap")
            print_board(state)
        else:  # NO TRIGGER

            if not is_board_empty(state):
                # Punnish / -REWARD to opp for missing trap. Not on first turn.
                qtable[opp_state][opp_action] += MISS_REWARD
                print(" NICE! :-) You dodged the trap!")

            # ***---RULE 4 enforcement---***
            # To allow phase 2 or not!...***

            if only_one_empty(new_state):
                # Clear the TRIGGER/TRAP boards
                new_state[2] = new_state[1] = [[" ", " ", " "],
                                               [" ", " ", " "],
                                               [" ", " ", " "]]
                # And skip Phase 2
                print("We skip laying traps")
            else:
                # We are here and state is still a win-state?
                # Then plz skip Phase2.
                if win:
                    print("We skip phase 2. GAME OVER!")
                else:
                    # print("else: only_one_empty")
                    # PHASE 2 - Lay a trap!
                    str_state = str(new_state[:2])
                    if str_state not in qtable:
                        qtable[str_state] = np.zeros(xsize)

                    action_phase2 = LOG_ACTION[1]
                    # ****************** PHASE 2 COMPLETE ****************************AI
                    new_state = move_phase2(new_state, action_phase2)
                    # ****************************************************************
                    print("Player-X placed a trap!")
                    print_board(new_state)

            # PHASE 1 AND PHASE 2 COMPLETE
            # NOW TIME TO EVALUATE. How do we update the Q(S,A)?
            # With WIN/TIE-rewards or with Bellman?
            # Can only adjust Q-table from winners perspective.
            if is_gameover(new_state, win):

                if win:
                    qtable[str(state[:2])][action_index] = WIN_REWARD
                if is_tie(new_state):
                    qtable[str(state[:2])][action_index] = TIE_REWARD

                print("Looks like Game Over!")
            else:  # Game isn't over. Do Bellman equation.
                if str(new_state[:2]) not in qtable:
                    # Add the Board to the dict w/ value = empty 1x72 array
                    qtable[str(new_state[:2])] = np.zeros(xsize)

                pos_moves = np.array(possiblePos(new_state))
                max_value_new_state = np.max(qtable[str(new_state[:2])][pos_moves])
                value_current_state = qtable[str(state[:2])][action_index]
                print("max_Q(S',a) = ", str(max_value_new_state))
                print("old_Q(S,A) = ", str(value_current_state))
                # ----------------------------
                opp_state = str(state[:2])  # Will be the next
                opp_action = action_index  # opponent values.
                # ----------------------------
                # Update the Q(S,A) with Bellman Eq.
                qtable[str(state[:2])][action_index] = (1 - learning_rate) * value_current_state + (
                        learning_rate * gamma * max_value_new_state)
                print("new_Q(S,A) = ", str(qtable[str(state[:2])][action_index]))

            # Update again before kicking it to the next player
            state = new_state
            print("Last thing before switching turns-")
            if win:
                print("----------------------------------------------------------------------break#2 [cuz AI win]")
                break
            elif is_tie(state):
                print("-----------------------------------------------------------------------------break#3 [cuz AI tie]")
                break
            else:
                state = swapBoard_me_and_her(state)
                # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**



# ____________________________________________________________________________________________________________
# -----------------------NEXT GUY'S TURN-------------------------------------------------------------------   |
# ----------------------------------------- __________________________________________________________________|
# ------------------HUMAN TURN-------------|
# -----------------------------------------|

        ## IF IT'S NEW TO THE TABLE
        if str(state[:2]) not in qtable:
            # Add the Board to the dict w/ value = empty 1x72 array
            qtable[str(state[:2])] = np.zeros(xsize)

        # PHASE 1 - Place a soldier!
        print("\n \n PLACE A SOLDIER!")
        # ------------------------------------
        action_phase1 = human_turn(state, 'O')
        LOG_ACTION = np.zeros(2)
        LOG_ACTION[0] = action_phase1
        # ------------------------------------
        print("action phase1:" + str(action_phase1))
        # ******* NEW STATE *** PHASE 1 COMPLETE *************************HU
        new_state, win = move_phase1(state, action_phase1, -1)
        # ****************************************************************
        if str(new_state[:2]) not in qtable:
            # Add the Board to the dict w/ value = empty 1x72 array
            qtable[str(new_state[:2])] = np.zeros(xsize)


        print("PLAYER-O PLACED A SOLDIER ", str(win) )
        print_board(new_state)
        # Before trigger-test, check if state is full and already in tie/win state. if yes, yeet!
        if is_board_full(new_state):
            if win:
                print(
                    "-----------------------------------------------------------break#-1 --- GAME ENDS IN AUTO-WIN ---")
                qtable[opp_state][opp_action] = LOSE_REWARD
                break
            if is_tie(new_state):
                print(
                    "-----------------------------------------------------------------------break#0 --- GAME ENDS IN TIE")
                qtable[opp_state][opp_action] = TIE_REWARD
                break

        if trigger_test(new_state):
            # Should be X's turn now
            print("**TRAP TRIGGERED**")
            # TRAP TRIGGERED
            # Reward for opp's action-combo hitting
            qtable[opp_state][opp_action] = HIT_REWARD

            # Should be O's turn now. Randomly kills an 'X'.
            exp_exp_tradeoff = random.uniform(0, 1)  # Look at Table or Random.
            if exp_exp_tradeoff > 0.90:
                P2K = possiblePos2Kill(new_state, current_player)
                if win:
                    # KILL THE HERO SOLDIER
                    action_phase3 = action_phase1
                elif 4 in P2K:
                    action_phase3 = 4
                else:
                    action_phase3 = action_phase1
            # Else doing a random choice --> exploration
            else:
                action_phase3 = random.choice(possiblePos2Kill(new_state, -1))
            # ******************* PHASE 3 COMPLETE ***************************AI
            next_next_state, win = move_phase3(new_state, action_phase3)
            # ****************************************************************
            # FOR IF HE FAILED TO REMoVE a Win-contributing piece
            # AI can't learn from this part.
            if win:
                print(
                    "----------------------------------------------------------------------break#1 [cuz fail kill]")
                print("________________ \(^___^)/ ")
                print_board(next_next_state)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            else:
                new_state = next_next_state
                print("state minus a soldier")
                print_board(new_state)
            # ___________________________________________________________
            # PHASE 2.5 - Lay a trap! Back to O's
            print("\n \n TIME TO LAY A TRAP PLAYER-O! ;-)")
            new_state = empty_trapboard(new_state)
            # ---------------------------------------------
            action_phase2 = human_turn(new_state, 'O')
            LOG_ACTION[1] = action_phase2               # Beware Bug- actioncombo [same,same] not work.
            action_index = actioncombo_to_table_index(LOG_ACTION)
            # ---------------------------------------------
            print("action phase2.5:" + str(action_phase2))
            # ************** PHASE 2.5 COMPLETE ******************************HU
            next_board = move_phase2(new_state, action_phase2)
            # ****************************************************************
            # (^^)/ *Update* again before kicking it to the next player
            state = next_board
            state = swapBoard_me_and_her(state)
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**
        else: # TRIGGER_TEST FAILS
            # Punnish / -REWARD to opp for missing trap
            print(" NICE! :-) You dodged the trap!")
            qtable[opp_state][opp_action] = MISS_REWARD
            # ***...RULE 4 enforcement...***
            # To allow phase 2 or not!...***
            if only_one_empty(new_state):
                # Clear the TRIGGER/TRAP boards
                new_state[2] = new_state[1] = [[" ", " ", " "],
                                               [" ", " ", " "],
                                               [" ", " ", " "]]
                # And skip Phase 2
                print("We skip laying traps")
            else:
                # We are here and state is still a win-state?
                # Then plz skip Phase2.
                if win:
                    print("We skip phase 2. GAME OVER!")
                else:
                    str_state = str(new_state[:2])
                    if str_state not in qtable:
                        qtable[str_state] = np.zeros(xsize)

                    # PHASE 2 - Lay a trap!
                    print("\n \n TIME TO LAY A TRAP PLAYER-O! ;-)")
                    new_state = empty_trapboard(new_state)
                    # ---------------------------------------------
                    action_phase2 = human_turn(new_state, 'O')
                    LOG_ACTION[1] = action_phase2
                    action_index = actioncombo_to_table_index(LOG_ACTION)
                    # ---------------------------------------------
                    print("action phase2:" + str(action_phase2))
                    # ***************** PHASE 2 COMPLETE *****************************HU
                    new_state = move_phase2(new_state, action_phase2)
                    # ****************************************************************
                    print("new_state after phase 2: Player-O placed a trap!")
                    print_board(new_state)
            # Update and reward Q-table from losers perspective.
            if is_gameover(new_state, win):

                if win:
                    qtable[opp_state][opp_action] = LOSE_REWARD
                elif is_tie(new_state):
                    qtable[opp_state][opp_action] = TIE_REWARD

                print("Look like Game Over?")
            else:# Game isn't over.
                # _________________________________________________________________
                # After PHASE 2, if the game isn't over then update the Q-function
                # for the starting state. Q(S,A)

                if str(new_state[:2]) not in qtable:
                    # Add the Board to the dict w/ value = empty 1x72 array
                    qtable[str(new_state[:2])] = np.zeros(xsize)

                pos_moves = np.array(possiblePos(new_state))
                max_value_new_state = np.max(qtable[str(new_state[:2])][pos_moves])
                value_current_state = qtable[str(state[:2])][action_index]
                # ----------------------------
                opp_state = str(state[:2])  # Will be the next
                opp_action = action_index  # opponent values.
                # ----------------------------
                # Update the Q(S,A) with Bellman Eq.
                qtable[str(state[:2])][action_index] = (1 - learning_rate) * value_current_state + (
                        learning_rate * gamma * max_value_new_state)

            # (^^)/ *Update* again before kicking it to the next player
            state = new_state

            # ¤ Last task: Even though many slots are vacant. Did we win?
            if win:
                print(
                    "-----------------------------------------------------------------break#4 [cuz human too good]")
                print("________________ \(^___^)/ ")
                print_board(state)
                print("_________________ \(O _ -) ")
                print("Wow you're really good. You just beat a computer")
                break
            if is_tie(state):
                print("________________ \(^___^)/ ")
                print_board(state)
                print("_________________ \(O _ -) ")
                print("IT'S A DRAW / TIE")
            else:
                state = swapBoard_me_and_her(state) # <-- Usually the last line before AI's turn.
                # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**
    print("qtable length:", len(qtable))

playgame()


# --- LAST THINGS ----------

print("OK I save table NOT! [-^.^]/")
'''
t = time.localtime()
t_stamp = time.strftime("%b-%d-%Y_%H%M", t)

with open(filename, 'wb') as handle:
    pickle.dump(qtable, handle, protocol=pickle.HIGHEST_PROTOCOL)


for x in qtable:
    print(x, ":",qtable[x])
'''
