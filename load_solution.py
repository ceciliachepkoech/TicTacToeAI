from game import run_game
from strategy import play_move_interactive

from strategy_fast import (
    create_random_valid_strategy,
    play_move_ai,
    create_ai,
)
from functools import partial
import pickle
from play_ai_vs_ai_benchmark import run_benchmark_games

if __name__ == "__main__":

    with open("/Users/cecilia/PycharmProjects/TicTacToeEvo/saved_run/solutions-90000.dat", "rb") as file:

        # load saved population into a dictionary object
        loaded = pickle.load(file)
        best_score = min(loaded.keys())
        strategy = loaded[best_score]
        print(best_score)
        print(loaded)
        human_p1 = play_move_interactive
        ai_p2 = create_ai(strategy)
        run_benchmark_games(
            ai_p2, create_ai(create_random_valid_strategy(uniform=True))
        )
        run_benchmark_games(
            create_ai(create_random_valid_strategy(uniform=True)), ai_p2
        )
        run_benchmark_games(ai_p2, ai_p2)
        run_game(human_p1, ai_p2, verbose=True)
        run_game(ai_p2, human_p1, verbose=True)
