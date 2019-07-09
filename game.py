import pyautogui
import win32gui

# Disables fail safe
pyautogui.FAILSAFE = False


# Game class
class Game:

    # Constructor
    def __init__(self):

        # Set handle to null (None) for now
        self.hwnd = None

        # Tries to find the game
        def callback(hwnd, extra):
            # Gets position of this window
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y

            # If this window is bookworm adventures AND if rv is not all 0
            if "Bookworm Adventures" in win32gui.GetWindowText(hwnd) and not (x == 0 and y == 0 and w == 0 and h == 0):
                # Store handle
                self.hwnd = hwnd

        # Enumerate through windows
        win32gui.EnumWindows(callback, None)

    # Gets position of Bookworm window
    def get_bookworm_pos(self):

        # Gets position of this window
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        return x, y, w, h

    # Returns a screenshot of the grid
    def screenshot_grid(self):
        # Gets app position
        (appX, appY, appWidth, appHeight) = self.get_bookworm_pos()

        # Screenshot and return
        return pyautogui.screenshot(region=(appX + 304, appY + 335, 200, 203))

    # Returns a grid of letters given a screenshot of the grid
    def get_letters(self, screenshot):

        return []


'''
# Stores app position
(appX, appY, appWidth, appHeight) = getBookwormPos()

print(str(appX) + ", " + str(appY))

# Selects app
pyautogui.moveTo(appX, appY)
pyautogui.click()

# Screenshots
letters = 

index = 0
for (x, y, w, h) in pyautogui.locateAll("y.png", letters, grayscale=True, confidence=0.8):
	print((x,y,w,h))
	#pyautogui.screenshot(str(index) + ".png", region=(appX + 304 + x, appY + 335 + y, w, h))
	index += 1

	pyautogui.moveTo(appX + 304 + x, appY + 335 + y)
	pyautogui.click()
'''
