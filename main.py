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
from pyclick import HumanClicker
import matplotlib.pyplot as plt

# load all template images of the pieces found on the board
# TODO: Add the remaining pieces (last regular piece, jellyfish, crab)

template_1 = ("1", cv2.imread('./images/whiteblue_square.png', 0))
template_2 = ("2", cv2.imread('./images/greenblue_diamond.png', 0))
template_3 = ("3", cv2.imread('./images/lightdarkblue_circle.png', 0))
template_4 = ("4", cv2.imread('./images/lightyellow_circle.png', 0))
template_5 = ("5", cv2.imread('./images/darkblue_square.png', 0))
template_6 = ("6", cv2.imread('./images/lightblue_square.png', 0))
template_7 = ("7", cv2.imread('./images/puffer.png', 0))

# plt.imshow(template_7[1])
# plt.show()
# exit()

templates = [template_1, template_2, template_3, template_4, template_5, template_6, template_7]

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
            #cv2.imshow("Window", crop_img)  # (comment out if you want to see piece detection)
            #cv2.waitKey(500)
            #print(x,y)

        # this means that we are probably in a duty window or break, so we wait a bit and continue after
        if sum(max_vals) <= 230:
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
        #print(board_arr)
        # Generates every possible new state given the current board state
        # https://github.com/jmitash/BilgeBot/blob/master/src/com/knox/bilgebot/ScoreSearch.java
        states = []

        scores = []

        depth = 0
        max_depth = 5

        count = 0

        start_i = 0
        start_j = 0


        all_scores_and_moves = []

        while start_i != 11:
            i = start_i
            j = start_j

            moves = [(i, j)]
            #time_begin = time.time()
            # print("start")
            # print(board_arr)
            board_arr_move = make_move(board_arr, i, j)
            # print("move 1")
            # print(board_arr_move)
            while depth != max_depth:
                # This works but is definitely suboptimal
                combos, min_length, max_length = obtain_combos(board_arr_move)
                score = evaluation_function(combos, min_length, max_length)


                board_arr_move = clear_board(board_arr_move)


                #tn = time.time()
                #time.sleep(1)
                depth += 1
                j += 1

                if j == 5:
                    j = 0
                    i += 1
                board_arr_move = make_move(board_arr_move, i, j)

                # for kadfi in all_scores_and_moves:
                #     print("Score and move in list", kadfi)
                #     time.sleep(1)
                all_scores_and_moves.append((score - 2 * len(moves), copy.deepcopy(moves)))
                moves.append((i, j))
            #print(time.time()-tn)


            depth = 0
            start_j += 1

            if start_j == 5:
                start_j = 0
                start_i += 1


        # first sort on the top score
        scores_moves = sorted(all_scores_and_moves, key=itemgetter(0), reverse=True)


        top_score = scores_moves[0][0]

        # then check which of the top scores has the least amount of moves
        move_to_make = sorted([sm for sm in scores_moves if sm[0] == top_score], key=lambda x: len(x[1]))[0]
        print( sorted([sm for sm in scores_moves if sm[0] == top_score], key=lambda x: len(x[1]))[0])
        print(move_to_make)

        for move in move_to_make[1]:

            hc.move(((ppwinx + 120) + 45 * move[1], (ppwiny + 92) + 45 * move[0]), 0.2)
            hc.click()
            # 2 seconds of waiting for the board to clear
            time.sleep(2)
            # Check whether we are in a duty/break window before continuing
            img = np.array(sct.grab(bilge_puzzle))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            while in_break(img_gray, winW, winH, templates) <= 230:
                print("we're waiting in between moves")
                time.sleep(0.5)
                img = np.array(sct.grab(bilge_puzzle))
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)







cv2.destroyAllWindows()
exit()

