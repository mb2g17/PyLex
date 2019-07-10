import pyautogui
import win32gui
from math import floor

# Disables fail safe
pyautogui.FAILSAFE = False


# Game class
class Game:

    # Stores alphabet to iterate over, in a certain order
    alphabet = [
        'i',
        't',
        'l',
        'a',
        'r',
        'b',
        'c',
        'd',
        'f',
        'e',
        'g',
        'h',
        'j',
        'k',
        'm',
        'n',
        'o',
        'p',
        'q',
        's',
        'y',
        'u',
        'v',
        'w',
        'x',
        'z',
    ]

    # Constructor
    def __init__(self):
        # Set handle to null (None) for now
        self.hwnd = None

        # Tries to find the game
        def callback(hwnd, extra):
            # If this window is bookworm adventures AND if we haven't already found it
            if "Bookworm Adventures" in win32gui.GetWindowText(hwnd) and self.hwnd is None:
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

        # Stores a grid of spotted letters
        letter_grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

        # Gets tile width and height
        tile_width, tile_height = floor(screenshot.width / 4), floor(screenshot.height / 4)

        # Iterates through alphabet
        for char in self.alphabet:
            # Locates this character in this position
            for (x, y, w, h) in pyautogui.locateAll("resources/" + char + ".png", screenshot,
                                                    grayscale=True,
                                                    confidence=0.85):

                # Gets i and j
                i, j = x // tile_width, y // tile_height

                # Stores this letter at a certain position
                letter_grid[i][j] = char
                print((x, y, w, h, char))

        return letter_grid


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
