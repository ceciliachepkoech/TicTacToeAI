from game import run_game
from strategy import play_move_interactive


if __name__ == '__main__':
    human_p1 = play_move_interactive
    human_p2 = play_move_interactive
    run_game(human_p1, human_p2, verbose=True)