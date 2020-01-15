import mss
import cv2
import time
import win32gui
import copy

import numpy as np

from operator import itemgetter
from funcs import sliding_window, in_break
from pywin32_grabwindow import obtain_pp_window_location
from analyze_board_state import obtain_combos, evaluation_function, get_chain_indices, \
                                    make_move, move_to_back, clear_board

from board import Board

from pyclick import HumanClicker
import matplotlib.pyplot as plt

# load all template images of the pieces found on the board
# TODO: Add the remaining pieces (last regular piece, jellyfish, crab)

template_1 = ("1", cv2.imread('./images/whiteblue_square.png', 0))
template_2 = ("2", cv2.imread('./images/greenblue_diamond.png', 0))
template_3 = ("3", cv2.imread('./images/lightblue_circle.png', 0))
template_4 = ("4", cv2.imread('./images/lightyellow_circle.png', 0))
template_5 = ("5", cv2.imread('./images/darkblue_square.png', 0))
template_6 = ("6", cv2.imread('./images/lightblue_square.png', 0))
template_7 = ("7", cv2.imread('./images/lightblue_diamond.png', 0))
template_8 = ("7", cv2.imread('./images/puffer.png', 0))

# plt.imshow(template_7[1])
# plt.show()
# exit()

templates = [template_1, template_2, template_3, template_4, template_5, template_6, template_7, template_8]

winW = 280
winH = 560

hc = HumanClicker()

# Main loop
while True:
    # grab screen
    with mss.mss() as sct:

        # grab the x and y coordinates of the top-left of the Puzzle Pirates window
        ppwinx, ppwiny = obtain_pp_window_location()

        # Grab the exact window of where the bilge screen appears
        bilge_puzzle = {'top': ppwiny+72, 'left': ppwinx+92, 'width': winW-15, 'height': winH-20}

        img = np.array(sct.grab(bilge_puzzle))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        board = []
        matching = []
        max_vals = []
        # Analyze pieces on board by sliding over every piece individually and template matching them
        for (x, y, window) in sliding_window(start_x = 0,
                                             start_y = 0,
                                             image = img_gray,
                                             stepSize= 45,
                                             windowSize=(winW, winH)):
            crop_img = img_gray[y:y + 45, x:x + 45]

            # TODO: might possibly need colors to properly detect, need to check with all 9 possible pieces


            matching = []
            # Template matching of every individual piece on the board against the templates included from above
            for temp in templates:
                res = cv2.matchTemplate(crop_img, cv2.resize(temp[1], dsize=(45,45)), cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                matching.append((temp[0], max_val))
                max_vals.append(max_val)

            board.append(sorted(matching, key=itemgetter(1))[-1][0])

        # this means that we are probably in a duty window or break, so we wait a bit and continue after
        if sum(max_vals) <= 270:
            print("we're waiting before/after moves")
            time.sleep(0.5)
            continue

        # initialize array and set variables to obtain board state
        # TODO: Vectorize, probably won't make a huge difference in execution time
        board_arr = np.zeros((12, 6))
        count = 1
        line = 0
        row = []
        # generate board state per row and add to array accordingly
        for i in range(0, len(board)):

            row.append(board[i])

            if count % 6 == 0:
                board_arr[line, :] = row
                line += 1
                row = []

            count += 1

        max_score = 0
        max_score_board = None

        start_board = Board(board = board_arr)
        all_boards_d1 = []

        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            for j in [0, 1, 2, 3, 4]:
                board_d1 = make_move(start_board.board, i, j)

                combos, min_length, max_length, extra = obtain_combos(board_d1)
                score = evaluation_function(combos, min_length, max_length, extra)

                board_d1_clear = Board(move=(i, j), board=clear_board(board_d1), score=score)
                board_d1_clear.previous = start_board

                if score > max_score:
                    max_score = score
                    max_score_board = board_d1_clear

                all_boards_d1.append(board_d1_clear)

        all_boards_d2 = []

        for b in all_boards_d1:
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                for j in [0, 1, 2, 3, 4]:
                    board_d2 = make_move(b.board, i, j)

                    combos, min_length, max_length, extra = obtain_combos(board_d2)
                    score = evaluation_function(combos, min_length, max_length, extra)

                    board_d2_clear = Board(move=(i, j), board=clear_board(board_d2), score=score)
                    board_d2_clear.previous = b

                    if (score - 6) > max_score:
                        max_score = score
                        max_score_board = board_d2_clear

                    all_boards_d2.append(board_d2_clear)

        all_boards_d3 = []

        for b in all_boards_d2:
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                for j in [0, 1, 2, 3, 4]:
                    board_d3 = make_move(b.board, i, j)

                    combos, min_length, max_length, extra = obtain_combos(board_d3)
                    score = evaluation_function(combos, min_length, max_length, extra)
                    #print(score,i,j)
                    board_d3_clear = Board(move=(i, j), board=clear_board(board_d3), score=score)
                    board_d3_clear.previous = b

                    if (score - 8) > max_score:
                        max_score = score
                        max_score_board = board_d3_clear

                    all_boards_d3.append(board_d3_clear)

        moves_to_make = []
        while max_score_board.previous:
            moves_to_make.append(max_score_board.move)
            max_score_board = max_score_board.previous

        moves_to_make = moves_to_make[::-1]

        for move in moves_to_make:

            img = np.array(sct.grab(bilge_puzzle))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print(in_break(img_gray, winW, winH, templates))
            while in_break(img_gray, winW, winH, templates) <= 270:
                print("we're waiting in between moves")
                time.sleep(0.5)
                img = np.array(sct.grab(bilge_puzzle))
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            hc.move(((ppwinx + 120) + 45 * move[1], (ppwiny + 92) + 45 * move[0]), 0.2)
            hc.click()
            # 2 seconds of waiting for the board to clear
            time.sleep(1)
            # Check whether we are in a duty/break window before continuing








cv2.destroyAllWindows()
exit()

