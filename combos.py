# -------------------------------------------------------------------------------------------------------------------- #
# Creates patterns in numpy arrays of every possible combination you are able to achieve within the bilging puzzle.    #
# Was not fun to hand-code all of these and there must be a way to avoid doing this.                                   #
# -------------------------------------------------------------------------------------------------------------------- #

import numpy as np



# all possible 3x3s
def three_by_three():
    tbt = []

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {0} {0} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('{0} {0} {0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))
    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbt.append(np.array([np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {0} {0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    return tbt


# all possible 3x4s or 4x3s
def three_by_four():
    tbf = []

    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {0} {0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))
    for i in range(0,7+1):
        for j in range(0,7+1):
            if i != j:
                tbf.append(np.array([np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {0} {0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 12 12 {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))
    return tbf

# all possible 4x4s
def four_by_four():
    fbf = []
    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                fbf.append(np.array([np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                fbf.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                fbf.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    for i in range(1,7+1):
        for j in range(1,7+1):
            if i != j:
                fbf.append(np.array([np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('12 {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} {1}'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' '),
                                     np.fromstring('{0} 12'.format(i, j), dtype=int, sep=' ')
                                     ]))

    return fbf


def bingo():
    b = []
    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' ')]))
    # 0s more up and down
    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 {1} 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} 12 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {1} {1} {1}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{1} {1} {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 12 {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{1} {1} {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 {1} 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{1} {1} {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 12  {0}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{1} {1} {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {1} {0}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{1} {1} {1} {0}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' ')]
                                  ))
    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 {0} 12 12 12'.format(i, j), dtype=int, sep=' ')]))

    for i in range(0, 8):
        for j in range(0, 8):
            if i != j:
                b.append(np.array([np.fromstring('{0} {0} {0} {1} {1} {1}'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' '),
                                   np.fromstring('12 12 12 {1} 12 12'.format(i, j), dtype=int, sep=' ')]))
    return b
