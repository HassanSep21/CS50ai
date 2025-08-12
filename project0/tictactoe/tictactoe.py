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
    flat_board = sum(board, [])

    count_x = flat_board.count(X)
    count_o = flat_board.count(O)

    return X if count_x == count_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] or i < 0 or j < 0 or i > len(board) or j > len(board):
        raise ValueError("invalid action")

    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Rows
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]

    # Columns
    for j in range(len(board)):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]

    # Right Diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[1][1]

    # Left Diagonal
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for col in row:
            if col == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else -1 if winner(board) == O else 0


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    current_player = player(board)

    if terminal(board):
        return None

    elif current_player == X:
        max_v = -math.inf
        best_action = None
        for action in actions(board):
            v = min_value(result(board, action))
            if max_v < v:
                max_v = v
                best_action = action
                if max_v == 1:
                    return best_action
        return best_action

    else:
        min_v = math.inf
        best_action = None
        for action in actions(board):
            v = max_value(result(board, action))
            if min_v > v:
                min_v = v
                best_action = action
                if min_v == -1:
                    return best_action
        return best_action
