from gamestate import (
    empty_board,
    X_MARK,
    O_MARK,
    is_winning_state,
    board_to_string,
    DRAW,
)
from functools import partial


def run_game(p1_play_move, p2_play_move, verbose=False):
    board = empty_board()
    play_x = partial(p1_play_move, player=X_MARK)
    play_o = partial(p2_play_move, player=O_MARK)
    turn_count = 0
    winner = is_winning_state(board)

    if verbose:
        print(f"Turn {turn_count}")
        print(board_to_string(board))

    while not winner:
        if turn_count % 2 == 0:
            board = play_x(board)
        else:
            board = play_o(board)

        winner = is_winning_state(board)
        if verbose:
            print(f"Turn {turn_count}")
            print(board_to_string(board))
        turn_count += 1

    if verbose:
        if winner == DRAW:
            print("Draw!")
        else:
            print(f"{winner} wins!")

    return winner
