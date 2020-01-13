import numpy as np
from operator import itemgetter
from itertools import product
import cv2

# Function to slide over different windows of size windowSize and steps stepSize of an image.
def sliding_window(start_x, start_y, image, stepSize, windowSize):
	# slide a window across the image
	for y in range(start_y, image.shape[0], stepSize):
		for x in range(start_x, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def in_break(img, winW, winH, templates):
    max_vals = []
    for (x, y, window) in sliding_window(start_x=0,
                                         start_y=0,
                                         image=img,
                                         stepSize=45,
                                         windowSize=(winW, winH)):
        crop_img = img[y:y + 45, x:x + 45]

        for temp in templates:
            res = cv2.matchTemplate(crop_img, cv2.resize(temp[1], dsize=(45, 45)), cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            max_vals.append(max_val)

    return sum(max_vals)
    # if sum(max_vals) <= 50:
    #     return True
    # else:
    #     return False

