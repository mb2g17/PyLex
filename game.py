from time import sleep

import pyautogui
import pyscreeze
import pytesseract
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

    # Stores typing speed
    type_speed = 0.05

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

    # Screenshots the whole game
    def screenshot(self):
        # Focuses and sleep
        self.focus()
        sleep(0.1)

        # Screenshot
        return pyautogui.screenshot(region=self.get_bookworm_pos())

    # Returns a screenshot of the grid
    def screenshot_grid(self):
        # Gets app position
        (appX, appY, appWidth, appHeight) = self.get_bookworm_pos()

        # Focuses and sleep
        self.focus()
        sleep(0.1)

        # Screenshot and return
        return pyautogui.screenshot(region=(appX + 304, appY + 335, 200, 203))

    # Returns a filtered screenshot of the grid, in pure black
    def screenshot_grid_filtered(self, threshold):
        # Gets screenshot of grid
        screenshot = self.screenshot_grid()

        # Filter only black
        for i in range(screenshot.width):
            for j in range(screenshot.height):
                (r, g, b) = screenshot.getpixel((i, j))
                if r > threshold or g > threshold or b > threshold:
                    screenshot.putpixel((i, j), (255, 255, 255))

        # Returns new image
        return screenshot

    # Returns a grid of letters given a screenshot of the grid (using tesseract)
    def get_letters_tesseract(self, screenshot):
        # Stores a grid of spotted letters
        letter_grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

        # Gets text
        text = pytesseract.image_to_string(screenshot, lang="Cooper")

        # Remembers indexes and previous char
        i = 0
        j = 0
        prev_i = 0
        prev_j = 0
        prev_char = ''

        # Goes through each character
        for char in text:
            # If it's an actual letter
            if char.isalpha():

                # Convert to lower
                char = char.lower()

                # If this is u and prev char was q, do nothing
                if not (char == 'u' and prev_char == 'q'):

                    # Store in grid, if indexes are not too big
                    if j < 4:
                        letter_grid[i][j] = char

                    # Stores previous char and indexes
                    prev_char = char
                    prev_i = i
                    prev_j = j

                    # Increase index
                    i += 1
                    if i == 4:
                        i = 0
                        j += 1

        # Return grid
        return letter_grid

    # Returns a grid of letters given a screenshot of the grid (using pyautogui)
    def get_letters_pyautogui(self, screenshot):

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

        return letter_grid

    # Focuses the game by clicking on it
    def focus(self):
        # Gets app position
        (appX, appY, appWidth, appHeight) = self.get_bookworm_pos()
        pyautogui.click(appX + appWidth // 2,
                        appY + appHeight // 2,
                        duration=self.type_speed)

    # Types out a word on the grid given a list of positions (0,1), (2,3) etc.
    def type(self, positions):
        # Gets app position
        (appX, appY, appWidth, appHeight) = self.get_bookworm_pos()

        # For each position
        for (x, y) in positions:
            # Click there
            pyautogui.click(appX + 304 + 25 + x * 50,
                            appY + 335 + 25 + y * 50,
                            duration=self.type_speed)

    # Just presses enter, usually to apply a word
    def press_enter(self):
        pyautogui.press('enter')

    # Right clicks, usually to cancel a word
    def right_click(self):
        pyautogui.click(button='right')

    # Returns true if the attack button is enabled
    def is_attack_enabled(self):
        return pyautogui.locate("resources/attackEnabled.png", self.screenshot()) is not None


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
