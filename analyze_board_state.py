import numpy as np
from numba import jit


@jit(nopython=True)
def obtain_combos(board):
    combos = 0
    extra = 0
    chain_min = 1
    chain_max = 1

    for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        board_row = board[n, :]
        chain = 1
        for i in [1, 2, 3, 4, 5]:
            if board_row[i - 1] == 24:
                extra += 0.2
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

    for n in [1, 2, 3, 4, 5]:
        board_col = board[:, n]
        chain = 1
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            if board_col[i - 1] == 24:
                extra += 0.2
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

def make_move(board, i, j):
    if board[i, j] == 8:
        board_copy = np.copy(board)
        board_copy_puffer = puffer_move(board_copy, i, j)

        return board_copy_puffer

    elif (board[i, j] == 9) or (board[i, j + 1] == 9):

        return np.copy(board)

    elif board[i, j] == 10:
        board_copy = np.copy(board)
        board_copy_jellyfish = jellyfish_move(board_copy, i, j + 1)

        return board_copy_jellyfish

    elif board[i, j + 1] == 10:
        board_copy = np.copy(board)
        board_copy_jellyfish = jellyfish_move(board_copy, i, j)

        return board_copy_jellyfish

    else:
        board_copy = np.copy(board)
        board_copy[i, j], board_copy[i, j + 1] = board_copy[i, j + 1], board_copy[i, j]

        return board_copy


@jit(nopython=True)
def get_chain_indices(board):
    indices = []

    for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        board_row = board[n, :]
        chain = 1
        for i in [1, 2, 3, 4, 5]:
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

    for n in [0, 1, 2, 3, 4, 5]:
        board_col = board[:, n]
        chain = 1

        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
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

@jit(nopython=True)
def _move_to_back(a, value):
    count = 0
    for x in a:
        if x != value:
            yield x
        else:
            count += 1
    for _ in range(count):
        yield value

@jit(nopython=True)
def move_to_back(a, value):
    return list(_move_to_back(a, value))

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


@jit(nopython=True)
def puffer_move(board, i, j):

    # puffer is at index (i,j). Remove 3x3 around puffer.

    min_col = max(0, j - 1)
    max_col = min(5, j + 2)

    min_row = max(0, i - 1)
    max_row = min(11, i + 1)

    # start with 3 above:
    board[min_row, min_col:max_col] = 24

    # then same line
    board[i, min_col:max_col] = 24

    # then bottom
    board[max_row, min_col:max_col] = 24

    return board

def jellyfish_move(board, i, j):
    piece_to_delete = board[i, j]

    mask = board == piece_to_delete
    board[mask] = 24

    return board