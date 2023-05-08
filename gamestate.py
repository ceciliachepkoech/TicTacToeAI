# Modules for the game state, moves and boards
from collections import defaultdict
from dataclasses import dataclass


def create_move(player, row, col):
    """
    Create a representation of a move on the tic tac toe board
    """
    return (player, row, col)


FREE = "_"
X_MARK = "X"
O_MARK = "O"
DRAW = "DRAW"


def _board2int(b):
    # Converts a board to a tuple of 9 ints for consistent comparision
    l = []
    for r in range(len(b)):
        for c in range(len(b[0])):
            l.append(ord(b[r][c]))
    return tuple(l)


def _move2int(m):
    # Converts a move to a tuple of 3 ints for consistent comparision
    p, r, c = m
    return (ord(p), r, c)


def sort_moves(lom):
    return sorted(lom, key=_move2int)


def sort_boards(lob):
    return sorted(lob, key=_board2int)


def next_player(mark):
    if mark == X_MARK:
        return O_MARK
    elif mark == O_MARK:
        return X_MARK
    raise Exception(f"Not a valid mark: {mark}")


def empty_board():
    return ((FREE, FREE, FREE), (FREE, FREE, FREE), (FREE, FREE, FREE))


__apply_move_memo = {}


def __unsafe_board_move(board, move):
    """
    INTERNAL FUNCTION: does a move on the board without checking that its a valid move
    Produces the new board, after the given move is applied.
    Results are cached for performance.
    """
    if (board, move) in __apply_move_memo:
        return __apply_move_memo[(board, move)]
    else:
        player, row, col = move
        mutable_board = list(map(list, board))
        mutable_board[row][col] = player
        new_board = tuple(map(tuple, mutable_board))
        __apply_move_memo[(board, move)] = new_board
        return new_board


def board_to_string(board):
    pretty_board = ""
    for row in board:
        pretty_board += " | ".join(row) + "\n"
    return pretty_board


__is_winning_state_memo = {}


def is_winning_state(board):
    """
    Is the board is a winning state? Produces False if not.
    Otherwise, produces the winning player, X_MARK or O_MARK or DRAW.
    Invariant: board is not in a state where two players are simultaneously winning
    Results are cached for performance.
    """
    if board in __is_winning_state_memo:
        return __is_winning_state_memo[board]
    else:
        res = __rows(board) or __cols(board) or __diagonals(board) or __draw(board)
        __is_winning_state_memo[board] = res
        return res


def __rows(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != FREE:
            return row[0]
    return False


def __cols(board):
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != FREE:
            return board[0][col]
    return False


def __diagonals(board):
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != FREE:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != FREE:
        return board[0][2]
    return False


def __draw(board):
    # Any empty spots?
    for row in board:
        if any([mark == FREE for mark in row]):
            return False
    return DRAW


# Internal variables, populated by __init_all_possible_boards_and_moves_from
__all_boards = set()
__valid_moves_for_board = defaultdict(set)
__winning_boards = set()


def __init_board_search(board, player):
    """ From an initial state, what possible boards are there? """

    if board in __all_boards or is_winning_state(board):
        __winning_boards.add(board)
        __all_boards.add(board)
        return

    __all_boards.add(board)

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == FREE:
                move = create_move(player, row, col)
                __valid_moves_for_board[board].add(move)
                __init_board_search(
                    __unsafe_board_move(board, move), next_player(player)
                )
    return


__init_board_search(empty_board(), X_MARK)


def all_board_states():
    return sort_boards(__all_boards)


def valid_moves(board):
    return sort_moves(__valid_moves_for_board[board])


def board_move(board, move):
    if move not in valid_moves(board):
        raise Exception(f"Illegal move: {move}")
    return __unsafe_board_move(board, move)
