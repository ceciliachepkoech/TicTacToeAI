import random
import time
from copy import deepcopy
from gamestate import (
    board_move,
    create_move,
    all_board_states,
    valid_moves,
    board_to_string,
    sort_moves,
)
import numpy as np

# Map all boards to a natural number (N)
# Map all moves to a natural number (M)
# A Strategy is an (N by M) matrix


ALL_BOARDS = all_board_states()
ALL_MOVES = []
for b in all_board_states():
    ALL_MOVES += valid_moves(b)

ALL_BOARDS = list(ALL_BOARDS)
ALL_MOVES = sort_moves(set(ALL_MOVES))

N_BOARDS = len(ALL_BOARDS)
N_MOVES = len(ALL_MOVES)

board2id = {}
move2id = {}
for i, b in enumerate(ALL_BOARDS):
    board2id[b] = i
for i, m in enumerate(ALL_MOVES):
    move2id[m] = i


valid_mask = np.zeros((N_BOARDS, N_MOVES))
for board in ALL_BOARDS:
    board_idx = board2id[board]
    moves = valid_moves(board)

    for move in valid_moves(board):
        move_idx = move2id[move]
        valid_mask[board_idx][move_idx] = 1


def create_ai(strategy):
    def play_move(board, player):
        return play_move_ai(board, player, strategy)

    return play_move


def play_move_ai(board, player, strategy):
    move_probabilities = strategy[board2id[board]]
    probs = move_probabilities
    valid = valid_moves(board)
    valid_idxes = [move2id[m] for m in valid]

    valid_probs = probs[valid_idxes]

    if valid_probs.sum() <= 0.9 or valid_probs.sum() >= 1.1:
        raise Exception(
            f"Not a valid probability dist  {valid_probs.sum()}| {valid_probs}\n{board_to_string(board)}\n{valid}\n {strategy}\n {probs}\n{valid_probs}"
        )

    move = random.choices(valid, valid_probs)[0]

    if player != move[0]:
        raise Exception("AI produced a move for the wrong player!")
    return board_move(board, move)


def normalize(strategy):
    for idx in range(N_BOARDS):
        total = strategy[idx].sum()
        if total > 0.00001:
            strategy[idx] = strategy[idx] / total
    return strategy


def create_random_valid_strategy(uniform=True):
    strategy = np.zeros((N_BOARDS, N_MOVES))

    for board in ALL_BOARDS:
        board_idx = board2id[board]
        moves = valid_moves(board)

        for move in valid_moves(board):
            move_idx = move2id[move]
            strategy[board_idx][move_idx] = 1 if uniform else 0.01 + np.random.random()

    strategy = normalize(strategy)
    return strategy


def add_noise_to_strategy(strategy, delta):
    # Additive

    new_strategy = deepcopy(strategy)
    mult_noise = np.random.uniform(1 - delta, 1 + delta, (N_BOARDS, N_MOVES))
    new_strategy = new_strategy + (valid_mask * mult_noise)

    new_strategy = normalize(new_strategy.clip(0))
    return new_strategy


def add_noise_to_strategy_mult(strategy, delta=0.1):
    # Multipliciative noise
    start = time.time()
    new_strategy = deepcopy(strategy)
    mult_noise = np.random.uniform(1 - delta, 1 + delta, (N_BOARDS, N_MOVES))
    new_strategy = np.multiply(new_strategy, mult_noise)

    new_strategy = normalize(new_strategy)

    dur = time.time() - start
    return new_strategy
