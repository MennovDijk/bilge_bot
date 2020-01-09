import mss
import cv2
import time
import win32gui

import numpy as np

from operator import itemgetter
from funcs import sliding_window, find_longest_island_indices
from pywin32_grabwindow import obtain_pp_window_location
from analyze_board_state import obtain_combos, evaluation_function
from pyclick import HumanClicker

# load all template images of the pieces found on the board
# TODO: Add the remaining pieces (last regular piece, pufferfish, jellyfish, crab)

template_1 = ("1", cv2.imread('./images/whiteblue_square.png', 0))
template_2 = ("2", cv2.imread('./images/greenblue_diamond.png', 0))
template_3 = ("3", cv2.imread('./images/lightdarkblue_circle.png', 0))
template_4 = ("4", cv2.imread('./images/lightyellow_circle.png', 0))
template_5 = ("5", cv2.imread('./images/darkblue_square.png', 0))
template_6 = ("6", cv2.imread('./images/lightblue_square.png', 0))

templates = [template_1, template_2, template_3, template_4, template_5, template_6]

winW = 280
winH = 560

hc = HumanClicker()

# Main loop
while True:
    # grab screen
    with mss.mss() as sct:
        time_begin = time.time()

        # grab the x and y coordinates of the top-left of the Puzzle Pirates window
        ppwinx, ppwiny = obtain_pp_window_location()

        # Grab the exact window of where the bilge screen appears
        bilge_puzzle = {'top': ppwiny+72, 'left': ppwinx+92, 'width': winW-15, 'height': winH-20}

        img = np.array(sct.grab(bilge_puzzle))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        board = []
        # Analyze pieces on board by sliding over every piece individually and template matching them
        for (x, y, window) in sliding_window(start_x = 0,
                                             start_y = 0,
                                             image = img_gray,
                                             stepSize= 45,
                                             windowSize=(winW, winH)):
            crop_img = img_gray[y:y + 45, x:x + 45]

            # TODO: might possibly need colors to properly detect, need to check with all 9 possible pieces


            matching = []
            max_vals = []
            # Template matching of every individual piece on the board against the templates included from above
            for temp in templates:
                res = cv2.matchTemplate(crop_img, cv2.resize(temp[1], dsize=(45,45)), cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                #print(min_val, max_val, min_loc, max_loc)
                matching.append((temp[0], max_val))
                max_vals.append(max_val)
            board.append(sorted(matching, key=itemgetter(1))[-1][0])
            # cv2.imshow("Window", crop_img)  # (comment out if you want to see piece detection)
            # cv2.waitKey(1)

        # this means that we are probably in a duty window or break, so we wait a bit and continue after
        if sum(max_vals) <= 2:
            print("we're waiting...")
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

        # Generates every possible new state given the current board state
        # https://github.com/jmitash/BilgeBot/blob/master/src/com/knox/bilgebot/ScoreSearch.java
        states = []

        scores = []


        # for all pieces on the original board

        depth = 0
        max_depth = 5

        count = 0
        print(board_arr)
        start_i = 0
        start_j = 0
        print("hey")
        while start_i != 11:

            board_arr_move = np.copy(board_arr)
            i = start_i
            j = start_j

            moves = [(i, j)]

            while depth != max_depth:

                # print(board_arr_move)

                board_arr_move[i, j], board_arr_move[i, j + 1] = board_arr_move[i, j + 1], board_arr_move[i, j]
                # combo detection works but something is wrong with the moves it gives me back
                #print(board_arr_move)
                combos, min_length, max_length = obtain_combos(board_arr_move)
                #print(combos,min_length,max_length)
                score = evaluation_function(combos, min_length, max_length)
                #print(score)
                if score >= 18:
                    print(board_arr_move)
                    break

                outs = [(find_longest_island_indices(board_arr_move, np.unique(board_arr_move)), "c"),
                        (find_longest_island_indices(board_arr_move.T, np.unique(board_arr_move)), "r")]

                # Bilging game logic that handles how the board changes when 3+ in a row get cleared
                # Keeps running when more than 3 pieces are matched either in columns or in rows
                while outs[0][0][0][0] >= 3 or outs[1][0][0][0] >= 3:

                    for out, r_c in outs:
                        if r_c == "r":  # checks rows
                            # if more than three of the same pieces in a row
                            if out[0][0] >= 3:
                                # because we're looking for rows here we need to transpose the array first
                                board_arr_move = board_arr_move.T

                                # set the value of the matching pieces to 24 (this is the "wildcard")
                                for x, y in out[0][1]:
                                    board_arr_move[x, y] = 24

                                # Moves all pieces underneath the matching pieces up by how many pieces are matched
                                board_arr_move = board_arr_move.T
                                ar = np.arange(board_arr_move.shape[1])
                                a = (board_arr_move == 24).argsort(0, kind='mergesort')
                                board_arr_move[:] = board_arr_move[a, ar]

                        if r_c == "c":  # checks columns
                            if out[0][0] >= 3:
                                for x, y in out[0][1]:
                                    board_arr_move[x, y] = 24

                                ar = np.arange(board_arr_move.shape[1])
                                a = (board_arr_move == 24).argsort(0, kind='mergesort')
                                board_arr_move[:] = board_arr_move[a, ar]

                    outs = [(find_longest_island_indices(board_arr_move, np.unique(board_arr_move)), "c"),
                            (find_longest_island_indices(board_arr_move.T, np.unique(board_arr_move)), "r")]

                depth += 1
                j += 1

                if j == 5:
                    j = 0
                    i += 1

                moves.append((i, j))

            depth = 0
            start_j += 1

            if start_j == 5:
                start_j = 0
                start_i += 1

            if score >= 18:
                #print(moves)
                for move in moves:
                    print(move)
                    hc.move((ppwinx + 110, ppwiny + 90), 0.1)

                    hc.move(((ppwinx + 120) + 45*move[1], (ppwiny + 92) + 45*move[0]), 0.2)
                    hc.click()

                    time.sleep(5)
                board_arr_move = np.copy(board_arr)
                break



cv2.destroyAllWindows()
exit()

