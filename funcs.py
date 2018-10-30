import numpy as np
from operator import itemgetter
from itertools import product

# Function to slide over different windows of size windowSize and steps stepSize of an image.
def sliding_window(start_x, start_y, image, stepSize, windowSize):
	# slide a window across the image
	for y in range(start_y, image.shape[0], stepSize):
		for x in range(start_x, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

# Function that finds the longest row of every value provided in a column of numpy array and their respective indices
# in that array
# E.G.
# [1, 3, 4, 5]
# [2, 4, 4, 2]
# [2, 3, 4, 1]
# [1, 2, 4, 1]
# Would return for the value 4; L = 4, indices = (0,2), (1,2), (2,2), (3,2)
# Would return for the value 5; L = 1, indices = (0,3)
def find_longest_island_indices(a, values):
    if 24 in values:
        values = values[:-1]
    b = np.pad(a, ((1,1),(0,0)), 'constant')
    shp = np.array(b.shape)[::-1] - [0,1]
    final_out = []
    for v in values:
        m = b==v
        idx = np.flatnonzero((m[:-1] != m[1:]).T)
        s0,s1 = idx[::2], idx[1::2]
        l = s1-s0
        maxidx = l.argmax()
        longest_island_flatidx = np.r_[s0[maxidx]:s1[maxidx]]
        out = np.c_[np.unravel_index(longest_island_flatidx, shp)][:,::-1]
        final_out.append((l[maxidx], list(out), v))

    return sorted(final_out,key=itemgetter(0))[::-1]


def match_pattern(input_array, pattern):

    pattern_shape = pattern.shape
    input_shape = input_array.shape

    is_wildcard = (pattern == 12) # This gets a boolean N-dim array where 12 is the wildcard value

    if len(pattern_shape) != len(input_shape):
        raise ValueError("Input array and pattern must have the same dimension")

    shape_difference = [i_s - p_s for i_s, p_s in zip(input_shape, pattern_shape)]

    if any((diff < -1 for diff in shape_difference)):
        raise ValueError("Input array cannot be smaller than pattern in any dimension")

    dimension_iterators = [range(0, s_diff + 1) for s_diff in shape_difference]

    # This loop will iterate over every possible "window" given the shape of the pattern
    for start_indexes in product(*dimension_iterators):
        range_indexes = [slice(start_i, start_i + p_s) for start_i, p_s in zip(start_indexes, pattern_shape)]
        input_match_candidate = input_array[range_indexes]

        # This checks that for the current "window" - the candidate - every element is equal
        #  to the pattern OR the element in the pattern is a wildcard
        if np.all(
            np.logical_or(
                is_wildcard, (input_match_candidate == pattern)
            )
        ):
            return True

    return False