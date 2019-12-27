import win32gui




def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))

def main():
    win32gui.EnumWindows(callback, None)

win32gui.EnumWindows(callback, None)


hwnd = win32gui.FindWindow("SunAwtFrame", None)
print(hwnd)
rect = win32gui.GetWindowRect(hwnd)
print(win32gui.GetWindowText(hwnd))
print(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])
