# Benchmark suite to test how performant the current implementation of games is
# see how good it runs as if you had infinite time
import time
from game import run_game
from strategy import create_random_valid_strategy, create_ai, add_noise_to_strategy
from strategy_fast import create_random_valid_strategy as create_random_valid_strategy_fast, create_ai as create_ai_fast, add_noise_to_strategy as add_noise_to_strategy_fast

from functools import partial
from collections import Counter

N = 10_000
M = 1_0

def run_benchmark_noise(init_s, add_noise):
    s = init_s
    print(f'Benchmarking the performance M={M} random modifications')
    start = time.time()
    for _ in range(M):
        s = add_noise(s)
    duration = time.time() - start
    print(f'Done in {duration} seconds')


def run_benchmark_games(p1, p2):
    print(f'Benchmarking the performance of running N={N} games')
    start = time.time()
    stats = Counter()
    for _ in range(N):
        result = run_game(p1, p2, verbose=False)
        stats.update([result])
    duration = time.time() - start
    print(f'Done in {duration} seconds')
    print(f'Approx. {N / (duration)} games completed per second')
    print(f"Total score: (N={N})")
    print(f"X wins:\t{stats['X']}\t({stats['X'] / N})")
    print(f"O wins:\t{stats['O']}\t({stats['O'] / N})")
    print(f"Draw:\t{stats['DRAW']}\t({stats['DRAW'] / N})")






if __name__ == '__main__':

    naive_strat = create_random_valid_strategy(uniform=True)
    fast_strat = create_random_valid_strategy_fast(uniform=True)
    p1 = create_ai(naive_strat)
    p2 = create_ai(naive_strat)
    p1_fast = create_ai_fast(fast_strat)
    p2_fast = create_ai_fast(fast_strat)

    # Numpy :
    print("NUMPY")
    print("-------------------")
    run_benchmark_games(p1_fast, p2_fast)
    run_benchmark_noise(fast_strat, add_noise_to_strategy_fast)

    # Dict: 40-60s
    print("DICT")
    print("-------------------")
    run_benchmark_games(p1, p2)
    run_benchmark_noise(naive_strat, add_noise_to_strategy)

