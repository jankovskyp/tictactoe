"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_counter = 0
    o_counter = 0

    for row in board:
        for column in row:
            if column == X:
                x_counter += 1
            if column == O:
                o_counter += 1

    # player O plays only when having less moves than player X
    if (x_counter == o_counter) or (x_counter == 0 and o_counter == 0):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    empty_cells = []

    for row_index in range(3):
        for column_index in range(3):
            if board[row_index][column_index] == EMPTY:
                empty_cells.append((row_index, column_index))

    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    action_row = action[0]
    action_cell = action[1]

    if new_board[action_row][action_cell] != EMPTY:
        raise Exception('Not a valid action for this board!')
    else:
        new_board[action_row][action_cell] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if (check_board_for_winner(board, X)):
        return X
    if (check_board_for_winner(board, O)):
        return O

    return None


def check_board_for_winner(board, player):
    """
    Check whether a concrete player won the game.
    """
    # checking for horizontals
    if (((board[0][0] == player) and (board[0][1] == player) and (board[0][2] == player)) or 
        ((board[1][0] == player) and (board[1][1] == player) and (board[1][2] == player)) or 
        ((board[2][0] == player) and (board[2][1] == player) and (board[2][2] == player))):
        return player
    # checking for verticals
    if (((board[0][0] == player) and (board[1][0] == player) and (board[2][0] == player)) or 
        ((board[0][1] == player) and (board[1][1] == player) and (board[2][1] == player)) or 
        ((board[0][2] == player) and (board[1][2] == player) and (board[2][2] == player))):
        return player
    # checking for diagonals
    if (((board[0][0] == player) and (board[1][1] == player) and (board[2][2] == player)) or 
        ((board[0][2] == player) and (board[1][1] == player) and (board[2][0] == player))):
        return player
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    has_empty_cells = False

    for row in board:
        if EMPTY in row:
            has_empty_cells = True
            break

    if not has_empty_cells:
        return True
    else:
        return winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    player_won = winner(board)
    if player_won == X:
        return 1
    if player_won == O:
        return -1
    
    return 0 # assuming that this will be called only for terminated boards


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None

    # Loops through next actions for the current board and creating a list of (utility, action)
    # Optional: there is a space for optimizing it by stopping the loop when the optimal solution was found
    evaluated_actions = []
    for action in actions(board):
        evaluated_actions.append((process_action(result(board, action)), action))
    
    # Sorting the actions by utility and returing the optimal action - MAX/last element for X and MIN/first element for O
    sorted_actions = sorted(evaluated_actions, key=lambda x: x[0])
    if player(board) == X:
        return  sorted_actions[len(sorted_actions)-1][1]
    else:
        return sorted_actions[0][1]


def process_action(board):
    """
    Method that recursively loops through the actions tree and returns the optimal utility for the current player
    """
    # When a terminal board is reached then returning the board's utility right away
    if terminal(board):
        return utility(board)

    default_x_utility = -math.inf
    default_o_utility = math.inf
    
    player_turn = player(board)
    
    # If not a terminal board then looping through next actions and selecting the MAX/MIN utility depending on the active player
    if player_turn == X:
        for action in actions(board):
            default_x_utility = max(default_x_utility, process_action(result(board, action)))
        return default_x_utility
    else:
        for action in actions(board):
            default_o_utility = min(default_o_utility, process_action(result(board, action)))
        return default_o_utility
            
