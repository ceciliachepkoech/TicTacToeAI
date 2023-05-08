import os
import time
from collections import Counter

from Evo import Evo
from game import run_game
from gamestate import O_MARK, X_MARK, DRAW
from play_ai_vs_ai_benchmark import run_benchmark_games
from strategy import play_move_interactive
from strategy_fast import (
    create_random_valid_strategy,
    add_noise_to_strategy,
    add_noise_to_strategy_mult,
    create_ai,
    normalize,
)
import random


# Hyperparameters
ROUNDS = 100
DELTA = 0.5
random_baseline_strategy = create_random_valid_strategy(uniform=True)


def objective_score(strategy, others):
    competitors = []
    # competitors = random.sample(list(others), min(1, len(others)))
    while len(competitors) < 1:
        competitors += [random_baseline_strategy]
    start = time.time()

    test_ai = create_ai(strategy)

    # Points (lower is better):
    # 0 for winning, 1 for drawing, 2 for losing
    stats_x = Counter()
    stats_o = Counter()
    for c in competitors:
        baseline_ai = create_ai(c)
        for _ in range(ROUNDS):
            # Run as X
            result_X = run_game(test_ai, baseline_ai, verbose=False)
            stats_x.update([result_X])
            # and again as O
            result_O = run_game(baseline_ai, test_ai, verbose=False)
            stats_o.update([result_O])

    n_losses = stats_x[O_MARK] + stats_o[X_MARK]
    n_draws = stats_x[DRAW] + stats_o[DRAW]

    duration = time.time() - start
    # print(f"Objective function ({duration}s)")
    # return (stats_x[O_MARK], stats_o[X_MARK], stats_x[DRAW], stats_o[DRAW])
    return (n_losses, n_draws)


def agent_add_noise(solutions):
    strategy = solutions[0]
    return add_noise_to_strategy(strategy, 0.1)


def agent_add_noise_mult(solutions):
    strategy = solutions[0]
    return add_noise_to_strategy_mult(strategy, 0.5)


def agent_merge(solutions):
    strategy1 = solutions[0]
    strategy2 = solutions[1]
    merged = strategy1 + strategy2

    merged = normalize(merged)

    return merged


def agent_reset(_solutions):
    return create_random_valid_strategy(uniform=False)


def main():
    # Create framework
    E = Evo()

    # Register some objectives
    E.add_fitness_criteria("score", objective_score)

    # Register some agents
    for i in range(6):
        # adds randomness with hopes of generating a better solution
        E.add_agent(f"add_noise_mult-{i}", agent_add_noise_mult, k=1)
    E.add_agent("add_noise", agent_add_noise, k=1)
    E.add_agent("merge_strategies", agent_merge, k=2)
    # flattens the distribution
    E.add_agent("reset", agent_reset, k=1)

    # Seed the population with initial random strategies
    for _ in range(10):
        E.add_solution(create_random_valid_strategy(uniform=False))

    # Run the evolver
    E.evolve(1_000_000, dom=1000, status=1000, sync=10_000, timeout=False)

    # Print final results
    for idx, sol in enumerate(E.pop.keys()):
        print(f"sol#{idx} =\t {sol}")

    best_strat = list(E.pop.values())[0]
    run_benchmark_games(create_ai(best_strat), create_ai(random_baseline_strategy))
    print("test it yourself:")

    while True:
        human_p1 = play_move_interactive
        human_p2 = create_ai(best_strat)
        run_game(human_p1, human_p2, verbose=True)


if __name__ == "__main__":

    main()

    # s = create_random_valid_strategy()
    # print(objective_score(s))
    #
    # for _ in range(10):
    #     s = add_noise_to_strategy(s)
    # print(objective_score(s))
