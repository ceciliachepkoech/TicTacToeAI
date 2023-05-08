from game import run_game
from strategy import play_move_interactive, create_random_valid_strategy, play_move_ai
from functools import partial


if __name__ == '__main__':
    human_p1 = play_move_interactive
    human_p2 = partial(play_move_ai, strategy=create_random_valid_strategy(uniform=False))
    run_game(human_p1, human_p2, verbose=True)