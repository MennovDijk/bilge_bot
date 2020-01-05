from pyclick import HumanClicker


# import numpy as np
# from funcs import match_pattern, find_longest_island_indices
# from itertools import product
# import time
#
#
#
# board = np.array([[1, 4, 2, 2, 3, 4],
#                   [3, 5, 5, 3, 2, 3],
#                   [3, 4, 5, 4, 5, 1],
#                   [1, 3, 1, 5, 2, 5],
#                   [4, 5, 5, 1, 4, 3],
#                   [1, 3, 2, 3, 4, 3],
#                   [3, 1, 5, 1, 1, 4],
#                   [2, 4, 5, 5, 2, 5],
#                   [3, 2, 5, 1, 1, 5],
#                   [5, 2, 5, 1, 4, 4],
#                   [2, 3, 1, 3, 5, 4],
#                   [3, 4, 2, 1, 4, 5]])
#
#
#
# outs = [(find_longest_island_indices(board, np.unique(board)), "c"),
#         (find_longest_island_indices(board.T, np.unique(board)), "r")]
#
# while outs[0][0][0][0] >= 3 or outs[1][0][0][0] >= 3:
#     print(outs[0][0][0][0], outs[1][0][0][0])
#
#     for out, r_c in outs:
#         if r_c == "r": # checks rows
#             if out[0][0] >= 3:
#                 board = board.T
#                 for x, y in out[0][1]:
#                     board[x, y] = 24
#
#                 board = board.T
#                 i = np.arange(board.shape[1])
#                 a = (board == 24).argsort(0, kind='mergesort')
#                 board[:] = board[a, i]
#
#         if r_c == "c": # checks columns
#             if out[0][0] >= 3:
#                 for x, y in out[0][1]:
#                     board[x, y] = 24
#
#                 i = np.arange(board.shape[1])
#                 a = (board == 24).argsort(0, kind='mergesort')
#                 board[:] = board[a, i]
#
#     outs = [(find_longest_island_indices(board, np.unique(board)), "c"),
#             (find_longest_island_indices(board.T, np.unique(board)), "r")]
#
#
# print(board)
#
# #while there is still a chain longer than 3 on the board (rotated or not)
# # # run
# # if out[0][0] >= 3:
# #     for x, y in out[0][1]:
# #         board[x, y] = 0
# #     i = np.arange(board.shape[1])
# #     a = (board == 0).argsort(0, kind='mergesort')
# #     board[:] = board[a, i]
# # then rotate the board and continue