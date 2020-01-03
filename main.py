import mss
import cv2
import time
import win32gui

import numpy as np

from operator import itemgetter
from funcs import sliding_window, find_longest_island_indices
from combos import three_by_three, three_by_four, four_by_four, bingo
from pywin32_grabwindow import obtain_pp_window_location

# load all template images of the pieces found on the board
# TODO: Add the remaining pieces (last regular piece, pufferfish, jellyfish, crab)

template_1 = ("1", cv2.imread('./images/whiteblue_square.png', 0))
template_2 = ("2", cv2.imread('./images/greenblue_diamond.png', 0))
template_3 = ("3", cv2.imread('./images/lightdarkblue_circle.png', 0))
template_4 = ("4", cv2.imread('./images/lightyellow_circle.png', 0))
template_5 = ("5", cv2.imread('./images/darkblue_square.png', 0))
template_6 = ("6", cv2.imread('./images/lightblue_square.png', 0))

templates = [template_1, template_2, template_3, template_4, template_5, template_6]

bingos = bingo()
three_by_threes = three_by_three()
three_by_fours = three_by_four()
four_by_fours = four_by_four()

winW = 280
winH = 560

# Main bot loop

def obtain_pp_window_location():
    """
    Returns X and Y coordinates of Puzzle Pirates window
    """
    # hwnd = win32gui.FindWindow("SunAwtFrame", None)
    hwnd = win32gui.FindWindow(None, "Puzzle Pirates - Zegelstein on the Emerald ocean")
    rect = win32gui.GetWindowRect(hwnd)
    
    return (rect[0], rect[1])


while True:
    # grab screen
    with mss.mss() as sct:
        time_begin = time.time()

        # grab the x and y coordinates of the top-left of the Puzzle Pirates window
        ppwinx, ppwiny = obtain_pp_window_location()

        # Grab the exact window of where the bilge screen appears
        bilge_puzzle = {'top': ppwiny+72, 'left': ppwinx+92, 'width': winW-15, 'height': winH-20}

        img = np.array(sct.grab(bilge_puzzle))

        board = []
        # Analyze pieces on board by sliding over every piece individually and template matching them
        for (x, y, window) in sliding_window(start_x = 0,
                                             start_y = 0,
                                             image = img,
                                             stepSize= 45,
                                             windowSize=(winW, winH)):

            crop_img = img[y:y + 45, x:x + 45]

            # TODO: might possibly need colors to properly detect, need to check with all 9 possible pieces
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            matching = []

            # Template matching of every individual piece on the board against the templates included from above
            for temp in templates:
                res = cv2.matchTemplate(crop_img, cv2.resize(temp[1], dsize=(45,45)), cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                matching.append((temp[0], max_val))

            board.append(sorted(matching, key=itemgetter(1))[-1][0])
            cv2.imshow("Window", crop_img)  # (comment out if you want to see piece detection)
            cv2.waitKey(10)

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
        print(board_arr)
        # Generates every possible new state given the current board state
        # TODO: Create evaluation function and apply depth-first tree search to find best states given depth of search D
        # https://github.com/jmitash/BilgeBot/blob/master/src/com/knox/bilgebot/ScoreSearch.java
        states = []

        # for all pieces on the original board
        for i in range(0, board_arr.shape[0]):
            for j in range(0, board_arr.shape[1] - 1):
                # copy original state
                board_arr_move = np.copy(board_arr)

                # make a move on the board (simply swap two pieces horizontally)
                board_arr_move[i, j], board_arr_move[i, j + 1] = board_arr_move[i, j + 1], \
                                                                                 board_arr_move[i, j]

                # TEST: matches the current board state against the predetermined combo's as specified in-game
                # Does work but currently EXTREMELY slow.
                # for tbf in three_by_fours:
                #     if match_pattern(board_arr_move, tbf):
                #         print(tbf)
                #         print("bingo!")


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

                # append the new game state to a list when sorting is completed
                states.append(((i,j),board_arr_move.astype(int)))

    # prints out all 60 obtained states for debugging purposes (should always be 60 since 12*5 possible moves)
    # print(len(states))
    # for (i,j), state in states:
    #     print((i,j))
    #     print(state)
    #     print("="*50)

    print(time.time() - time_begin) # Currently takes 0.4-0.5 seconds to run on my computer (= very slow)
    break

cv2.destroyAllWindows()
exit()

