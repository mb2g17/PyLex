import threading
from threading import Thread
from time import sleep

import pyautogui
import pyscreeze
import win32api
import win32con
import win32gui
import win32process
from PIL import Image
from math import floor

import cv2 as cv

# Disables fail safe
from locked_object import LockedObject

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
        'z'
    ]

    # Game version (1 for the first game, 2 for vol. 2)
    version = 1

    # Constructor, with process close event
    def __init__(self):
        # Set handle to null (None) for now
        self.hwnd = LockedObject()

    # Searches for the game window, takes in function event for when process closes
    def search_for_game_window(self, on_process_close):

        # If we've already found it, don't waste our time
        if self.hwnd.value_is_set():
            return

        # Tries to find the game
        def callback(hwnd, extra):

            # Gets properties from hwnd
            window_text = win32gui.GetWindowText(hwnd)
            is_window_visible = win32gui.IsWindowVisible(hwnd)

            self.hwnd.acquire_lock()
            is_handle_none = self.hwnd.get() is None
            self.hwnd.release_lock()

            # If the window name seems right AND this window is visible AND we haven't already found it
            if "Bookworm Adventures" in window_text and \
                    is_window_visible == 1 and \
                    is_handle_none:

                # Gets process name
                pid = win32process.GetWindowThreadProcessId(hwnd)
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False,
                                              pid[1])
                proc_name = win32process.GetModuleFileNameEx(handle, 0)
                proc_name = proc_name.split("\\")[::-1][0]

                # If the process name seems legit
                if "BookwormAdventures" in proc_name or "popcapgame1" in proc_name:

                    # Store handle, thread-safely
                    self.hwnd.acquire_lock()
                    self.hwnd.set(hwnd)
                    self.hwnd.release_lock()

                    # Starts a thread that will check when window is closed
                    def thread_process():
                        while True:
                            # Gets if window is still up, thread-safely
                            self.hwnd.acquire_lock()
                            is_window_condition = win32gui.IsWindow(self.hwnd.get())
                            self.hwnd.release_lock()

                            # If window is not up, say it is closed
                            if is_window_condition == 0:
                                on_process_close()
                                break
                            # If GUI thread is gone, kill self
                            elif not threading.main_thread().is_alive():
                                break
                            else:
                                sleep(1)
                    thread = Thread(target=thread_process)
                    thread.start()

                    # Stores version
                    if "Vol. 2" in window_text:
                        self.version = 2
                    else:
                        self.version = 1

        # Enumerate through windows
        win32gui.EnumWindows(callback, None)

    # Gets position of Bookworm window
    def get_bookworm_pos(self):

        # Gets rectangle of window, thread-safely
        self.hwnd.acquire_lock()
        rect = win32gui.GetWindowRect(self.hwnd.get())
        self.hwnd.release_lock()

        # Gets coords and sizes
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
        screenshot.save("screenshot.png")

        # Filter only black (old method)
        '''
        for i in range(screenshot.width):
            for j in range(screenshot.height):
                (r, g, b) = screenshot.getpixel((i, j))
                if r > threshold or g > threshold or b > threshold:
                    screenshot.putpixel((i, j), (255, 255, 255))
        '''
        # Filter only black (OpenCV method)
        img = cv.imread("screenshot.png", 0)
        ret, img = cv.threshold(img, threshold, 255, cv.THRESH_BINARY)
        cv.imwrite("screenshot.png", img)

        # Returns new image
        return Image.open("screenshot.png")

    # Returns a grid of letters given a screenshot of the grid (using pyautogui)
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
        for char in self.alphabet + ["wildcard"]:
            # Locates this character in this position
            for (x, y, w, h) in pyautogui.locateAll("resources/" + char + ".png", screenshot,
                                                    grayscale=True,
                                                    confidence=0.85):
                # Gets i and j
                i, j = x // tile_width, y // tile_height

                # Stores this letter at a certain position
                letter_grid[i][j] = char if char is not "wildcard" else "?"

        return letter_grid

    # Focuses the game
    def focus(self):
        self.hwnd.acquire_lock()
        win32gui.BringWindowToTop(self.hwnd.get())
        self.hwnd.release_lock()

    # Types out a word on the grid given a list of positions (0,1), (2,3) etc. and a speed
    def type(self, positions):
        # Gets app position
        (appX, appY, appWidth, appHeight) = self.get_bookworm_pos()

        # For each position
        for (x, y) in positions:
            # Click there
            pyautogui.click(appX + 304 + 25 + x * 50,
                            appY + 335 + 25 + y * 50)

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
