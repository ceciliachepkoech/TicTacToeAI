# just using dictionaries
# super slow

import random
from copy import deepcopy
from gamestate import board_move, create_move, all_board_states, valid_moves


def play_move_interactive(board, player):
    print("Your turn:")
    command = input("Input a coordinate row,col: (i.e. '1,2')\n")
    row, col = [int(token.strip()) for token in command.split(',')]
    move = create_move(player, row, col)
    return board_move(board, move)


def create_ai(strategy):
    def play_move(board, player):
        return play_move_ai(board, player, strategy)

    return play_move


def play_move_ai(board, player, strategy):
    move_probabilities = strategy[board]

    choices = list(move_probabilities.keys())
    probs = list(move_probabilities.values())
    if sum(probs) <= 0.9:
        raise Exception(f"dist not normalized: {probs}")
    move = random.choices(choices, probs)[0]
    if player != move[0]:
        raise Exception("AI produced a move for the wrong player!")
    return board_move(board, move)


def create_random_valid_strategy(uniform=True):
    strategy = dict()
    for board in all_board_states():
        move_probabilities = dict()
        moves = valid_moves(board)

        total = 0
        for move in moves:
            move_probabilities[move] = 1.0 if uniform else random.random()
            total += move_probabilities[move]

        # normalize
        for move in moves:
            move_probabilities[move] = move_probabilities[move] / total

        strategy[board] = move_probabilities
    return strategy


def add_noise_to_strategy(strategy, delta=0.1):
    new_strategy = deepcopy(strategy)

    for board in new_strategy.keys():
        total = 0
        for move in new_strategy[board]:
            # Introduce noise proportionate to delta and normalize
            new_weight = new_strategy[board][move] + random.uniform(-delta, delta)
            new_strategy[board][move] = max(new_weight, 0.01)  # Ensure weight is non-negative
            total += new_strategy[board][move]
        # normalize
        for move in new_strategy[board]:
            new_strategy[board][move] = new_strategy[board][move] / total
    return new_strategy
