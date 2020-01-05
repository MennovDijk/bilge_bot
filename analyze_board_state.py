import numpy as np
from numba import jit


@jit(nopython=True)
def obtain_combos(board):
    combos = 0
    chain_min = 1
    chain_max = 1

    # go over all rows
    board_length = 12
    chain = 1
    ridx = []

    for n in range(board_length):
        board_row = board[n, :]
        for i in range(1, len(board_row)):
            if board_row[i - 1] == board_row[i]:
                chain += 1
                if chain == 3:
                    board[n,(i-2,i-1,i)] = 24
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
    chain = 1

    for n in range(board_length):
        board_col = board[:, n]
        for i in range(1, len(board_col)):
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

    return combos, chain_min, chain_max


# this is incorrect but will serve for now
def evaluation_function(number_of_combos, chain_min, chain_max):
        return number_of_combos * chain_min * chain_max