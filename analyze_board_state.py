import numpy as np
from numba import jit


@jit(nopython=True)
def obtain_combos(board):
    combos = 0
    extra = 0
    chain_min = 1
    chain_max = 1

    # go over all rows
    board_length = 12

    for n in range(board_length):
        board_row = board[n, :]
        chain = 1
        for i in range(1, len(board_row)):
            if board_row[i-1] == 24:
                extra += 0.5
                continue
            if board_row[i - 1] == board_row[i]:
                chain += 1
                if chain == 3:
                    combos += 1
                    chain_min = 3
                    chain_max = 3
                elif chain == 4:
                    chain_max = 4
                elif chain == 5:
                    chain_max = 5
            else:
                chain = 1

    # go over all columns
    board_length = 6

    for n in range(board_length):
        board_col = board[:, n]
        chain = 1
        for i in range(1, len(board_col)):
            if board_col[i-1] == 24:
                extra += 0.5
                continue
            if board_col[i - 1] == board_col[i]:
                chain += 1
                if chain == 3:
                    combos += 1
                    chain_min = 3
                    chain_max = 3
                elif chain == 4:
                    chain_max = 4
                elif chain == 5:
                    chain_max = 5
            else:
                chain = 1

    return combos, chain_min, chain_max, extra


# this is incorrect but will serve for now
def evaluation_function(number_of_combos, chain_min, chain_max, extra):
        return number_of_combos * chain_min * chain_max + extra

@jit(nopython = True)
def make_move(board, i, j):
    board_copy = np.copy(board)
    board_copy[i, j], board_copy[i, j + 1] = board_copy[i, j + 1], board_copy[i, j]

    return board_copy


@jit(nopython=True)
def get_chain_indices(board):
    indices = []

    # go over all rows
    board_length = 12

    for n in range(board_length):
        board_row = board[n, :]
        chain = 1
        for i in range(1, len(board_row)):
            if board_row[i - 1] == 24:
                continue
            if board_row[i - 1] == board_row[i]:
                chain += 1
                if chain == 3:
                    indices.append((n, i - 2))
                    indices.append((n, i - 1))
                    indices.append((n, i))
                elif chain == 4:
                    indices.append((n, i))
                elif chain == 5:
                    indices.append((n, i))
            else:
                chain = 1

    # go over all columns
    board_length = 6

    for n in range(board_length):
        board_col = board[:, n]
        chain = 1
        for i in range(1, len(board_col)):
            if board_col[i - 1] == 24:
                continue
            if board_col[i - 1] == board_col[i]:
                chain += 1
                if chain == 3:
                    indices.append((i - 2, n))
                    indices.append((i - 1, n))
                    indices.append((i, n))
                elif chain == 4:
                    indices.append((i, n))
                elif chain == 5:
                    indices.append((i, n))
            else:
                chain = 1

    return indices

@jit(nopython = True)
def move_to_back(a, value):
    new_a = []

    total_values = 0

    for v in a:
        if v == value:
            total_values += 1
        else:
            new_a.append(v)

    return new_a + [value] * total_values

# JIT IT
def clear_board(board):
    indices = get_chain_indices(board)

    while indices:
        for idx in indices:
            board[idx[0], idx[1]] = 24

        for n in [0, 1, 2, 3, 4, 5]:
            board[:, n] = move_to_back(board[:, n], 24)

        indices = get_chain_indices(board)

    return board