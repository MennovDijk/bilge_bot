# Introduction
Solves the bilging puzzle within YPP Puzzle Pirates using a brute-force algorithm that analyzes all possible board states 3 moves in advance.

This program is fully functional, albeit suboptimal. It will get you good/excellent in duty reports and can obtain ranks up to renowned.

No manual input is required. The program will automatically pause when you do not have the bilging window opened.


# Dependencies
 - mss (pip install -U mss)
 - opencv (pip install opencv-python)
 - numpy (pip install numpy)
 - pyclick (pip install pyclick)
 - numba (pip install numba)
 
# Usage

- Start up the Puzzle Pirates client.
- Change the string in pywin32.grabwindow.py to match your Puzzle Pirates client (this requires you to only change the name and ocean you are playing on)
- Run the program.

# TODO

- Multithreading support
- Optimize existing code 
- Refactor code (yes, I am fully aware it is a mess right now).

**NOTE:** Making use of this script can (and probably will) lead to your account getting banned. I only undertook this project to learn more about algorithms and image processing. 
