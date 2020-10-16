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

    # Takes each board, saves the rows in a variable, then prints the variables
    for b in range(len(totalBoard)):
        firstRow = firstRow + "|" + " ".join(totalBoard[b][0]) + "|"
        secondRow = secondRow + "|" + " ".join(totalBoard[b][1]) + "|"
        thirdRow = thirdRow + "|" + " ".join(totalBoard[b][2]) + "|"

        # if 3 boards have been collected, then it prints the boards out
        # and resets the variables (firstRow, secondRow, etc.)
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
                #print("**TRAP TRIGGERED!** b[0]:"+ new_board[0][row][col] + " b[2]:"+ new_board[2][row][col])
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


# ______________________________________________________________________________________________________________________________________________[*_*]

# ---------------------------------------------------------------Q TABLE STUFF--------------------------------


qtable = {}

#filename = 'v2Q_TABLE_4_QTvRA_10k.pickle'
#filename = 'v3Q_TABLE_4_QTvRA_10kA.pickle'
#filename = 'v3Q_TABLE_4_QTvQT_20kC.pickle'
#filename = 'v3Q_TABLE_4_QTvQT_20kA.pickle'
#filename = 'please.pickle'
filename = 'v3Q_TABLE_4_QTvQT_20kB.pickle'

# LOAD Q TABLE
with open(filename, 'rb') as handle:
    qtable = pickle.load(handle)

total_episodes = 20000         # Total episodes
learning_rate = 0.9            # Learning rate 0.9
gamma = 0.95                # Discounting rate 0.95

# Exploration parameters
epsilon = 0.9                # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.0001            # Minimum exploration probability
decay_rate = 0.05            # Exponential decay rate for exploration prob

# List of rewards
WIN_REWARD = 1                  # 1
TIE_REWARD = 0.5                # 0.5
LOSE_REWARD = -1                # -1

HIT_REWARD = 0.8                # 0.8
MISS_REWARD = -0.15            # -0.15


# Analytical data
TOT_TIES = 0
X_WINS = 0
O_WINS = 0

# 2 For life or until learning is stopped
for episode in range(total_episodes):

    if episode % 100 == 0:
        print(episode)
    # Reset the environment
    state = get_empty_board()
    current_player = 1 # start a X
    xsize = 72
    opp_state = ""
    opp_action = 0

# _______________________________________________________________________________________*
# ----- THE GAMES BEGIN! ----------------------------------------------------------------*
# _______________________________________________________________________________________*
    while True:
        # New state for current player.
        str_state = str(state[:2])
        # New reset action index for current player.
        action_index = 0

        ## IF IT'S NEW TO THE TABLE
        if str_state not in qtable:
            # Add the Board to the dict w/ value = empty 1x9 array
#            print("NEW STATE ADDED 2")
            qtable[str_state] = np.zeros(xsize)

        ## If this number > greater than epsilon --> Use table. Else RANDOM.
        exp_exp_tradeoff = random.uniform(0, 1)
        # ------------- If player 'O' then always go random----
        if current_player == -1:
            exp_exp_tradeoff = 0.0
        # -----------------**----------**------------**--------
        if exp_exp_tradeoff > epsilon:
            # So... action_index = table_value basically
            action_index = best_action_from_table(state, qtable)
            LOG_ACTION = table_index_to_actioncombo(action_index)
            # LOG_ACTION = array([0, 1]) 4 example. Meaning place soldier at 0 and trap at 1.
            action_phase1 = LOG_ACTION[0]
        # Else doing a random choice --> exploration
        else:
            action_index = random.choice(possiblePos(state))
            LOG_ACTION = table_index_to_actioncombo(action_index)
            action_phase1 = LOG_ACTION[0]

        # ************* ** NEW STATE ** PHASE 1 COMPLETE ** ***************
        new_state, win = move_phase1(state, action_phase1, current_player)
        # *****************************************************************
#        print("PLAYER " + str(current_player) + " PLACED A SOLDIER")
#        print("new_state:")
#        print_board(new_state)
        # Before trigger-test, check if state is full board and already in tie/win state. if yes, yeet!
        if is_board_full(new_state):
            if win:
#                print("-----------------------------------------------------------break#-1 --- GAME ENDS IN AUTO-WIN")
                qtable[str(state[:2])][action_index] = WIN_REWARD
                qtable[opp_state][opp_action] = LOSE_REWARD
                if current_player == 1:
                    X_WINS += 1
                else:
                    O_WINS += 1
                break
            if is_tie(new_state):
#                print("-----------------------------------------------------------------------break#0 --- GAME ENDS IN TIE")
                qtable[str(state[:2])][action_index] = TIE_REWARD
                qtable[opp_state][opp_action] = TIE_REWARD
                TOT_TIES += 1
                break




        if trigger_test(new_state):
#            print("bling-blong TRAP TRIGGERED")
            # TRAP TRIGGERED
            # Reward for opp's action-combo hitting
            qtable[opp_state][opp_action] += HIT_REWARD

            # Should be O's turn now. Randomly kills an 'X'.
            exp_exp_tradeoff = random.uniform(0, 1) # Look at Table or Random.
            # ------------- If player 'O' then always go random----
            if current_player == 1:
                exp_exp_tradeoff = 0.0
            # -----------------**----------**------------**--------
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
                action_phase3 = random.choice(possiblePos2Kill(new_state, current_player))

            # ***************** PHASE 3 COMPLETE ******************************
            next_next_state, wonBoard = move_phase3(new_state, action_phase3)
            # *****************************************************************

            # FOR IF HE FAILED TO REMoVE a Win-contributing piece
            if wonBoard:
                qtable[str(state[:2])][action_index] = WIN_REWARD
#                print("----------------------------------------------------------------------break#1 [cuz fail kill]")
#                print_board(next_next_state)
                if current_player == 1:
                    X_WINS += 1
                else:
                    O_WINS += 1
                break
            else:
                new_state = next_next_state
                win = wonBoard
#                print("state minus a soldier")
#                print_board(new_state)


            # PHASE 2.5 - Lay a trap! Back to X's turn
            str_state = str(new_state[:2])
            if str_state not in qtable:
#                print("NEW STATE ADDED 3")
                qtable[str_state] = np.zeros(xsize)

            exp_exp_tradeoff = random.uniform(0, 1) # Look at Table or Random.
            # ------------- If player 'O' then always go random----
            if current_player == -1:
                exp_exp_tradeoff = 0.0
            # -----------------**----------**------------**--------
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

            # ************ PHASE 2.5 COMPLETE *********************************
            next_state = move_phase2(new_state, action_phase2)
            # *****************************************************************
            # Update again before kicking it to the next player
            state = next_state
#            print("After trigger. Time for ", str(current_player), " to lay his trap")
#            print_board(state)
        else: # NO TRIGGER! ** TRIGGER TEST NEGATIVE ***

            if not is_board_empty(state):
                # Punnish / -REWARD to opp for missing trap. Not on first turn.
                qtable[opp_state][opp_action] += MISS_REWARD

            # ***...RULE 4 enforcement...***
            # To allow phase 2 or not!...***
#            a = only_one_empty(new_state)
#            print("RULE4?",a)
            if only_one_empty(new_state):
                # Clear the TRIGGER/TRAP boards
                new_state[2] = new_state[1] = [[" ", " ", " "],
                                               [" ", " ", " "],
                                               [" ", " ", " "]]
                # And skip Phase 2
#                print("We skip laying traps")
            else:
                if win:
#                    print("We skip phase 2. GAME OVER!")
                    str_state = str(new_state[:2])
                else:
                    # PHASE 2 - Lay a trap!
                    str_state = str(new_state[:2])
                    if str_state not in qtable:
#                        print("NEW STATE ADDED 4")
                        qtable[str_state] = np.zeros(xsize)

                    action_phase2 = LOG_ACTION[1]
                    # **************** PHASE 2 COMPLETE *******************************
                    new_state = move_phase2(new_state, action_phase2)
                    # *****************************************************************
#                    print("new_state after phase 2:", str(current_player), " Placed a trap!")
#                    print_board(new_state)

            # PHASE 1 AND PHASE 2 COMPLETE
            # NOW TIME TO EVALUATE. How do we update the Q(S,A)? With WIN/TIE-rewards or with Bellman?
            if is_gameover(new_state, win):
                # Is it GAME OVER cuz we won or tied?
                if win:
                    qtable[str(state[:2])][action_index] = WIN_REWARD
                    qtable[opp_state][opp_action] = LOSE_REWARD
                if is_tie(new_state):
                    qtable[str(state[:2])][action_index] = TIE_REWARD
                    qtable[opp_state][opp_action] = TIE_REWARD
            else:  # Game isn't over.
                if str(new_state[:2]) not in qtable:
                    # Add the Board to the dict w/ value = empty 1x72 array
                    qtable[str(new_state[:2])] = np.zeros(xsize)
#                    print("NEW STATE ADDED 5")

                pos_moves = np.array(possiblePos(new_state))
                max_value_new_state = np.max(qtable[str(new_state[:2])][pos_moves])
                value_current_state = qtable[str(state[:2])][action_index]

                # ----------------------------
                opp_state = str(state[:2])  # Will be the next
                opp_action = action_index   # opponent values.
                # ----------------------------
                # Update the Q(S,A) with Bellman Eq.
                qtable[str(state[:2])][action_index] = (1 - learning_rate) * value_current_state + (
                        learning_rate * gamma * max_value_new_state)


            # Update again before kicking it to the next player
            state = new_state
 #           print("Last thing before switching turns-")
        # HERE WE BREAK! If Phase1 made a win-state and no traps were activated.
        if win:
#            print("----------------------------------------------------------------------break#2 [cuz win]")
            if current_player == 1:
                X_WINS += 1
            else:
                O_WINS += 1
            break
        # AND HERE WE BREAK! If Phase1 made a tie-state and no traps were activated.
        elif is_tie(state):
# #           print("-----------------------------------------------------------------------------break#3 [cuz tie]")
            TOT_TIES += 1
            break
        else:
            # NEXT GUY'S TURN
            current_player *= -1
            state = swapBoard_me_and_her(state)

    # Reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

# --- LAST THINGS ----------
print("Total Ties: ", TOT_TIES)

print("Total X (Q-table) wins: ", X_WINS)

print("Total O (pure random) wins: ", O_WINS)

print("qtable length:", len(qtable))

print("OK I save table now! [-^.^]/")
'''
t = time.localtime()
t_stamp = time.strftime("%b-%d-%Y_%H%M", t)
'''
filename = 'v3Q_TABLE_4_QTvRA_20kB.pickle'

with open(filename, 'wb') as handle:
    pickle.dump(qtable, handle, protocol=pickle.HIGHEST_PROTOCOL)

'''
for x in qtable:
    print(x, ":",qtable[x])
'''
