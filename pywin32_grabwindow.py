import win32gui

def obtain_pp_window_location():
    """
    Returns X and Y coordinates of Puzzle Pirates window
    """
    # hwnd = win32gui.FindWindow("SunAwtFrame", None)
    hwnd = win32gui.FindWindow(None, "Puzzle Pirates - Zegelstein on the Emerald ocean")
    rect = win32gui.GetWindowRect(hwnd)

    return (rect[0], rect[1])