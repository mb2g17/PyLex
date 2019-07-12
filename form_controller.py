from PIL import ImageEnhance, Image
from PyQt5 import QtGui
from time import sleep

import form_view
import game
import misc
import numpy

from threading import Thread


# Controller class
class UiController:

    # Constructor; adds view to window
    def __init__(self, window):

        # Creates the view
        self.form = form_view.Ui_Form()
        self.form.setupUi(window)

        # Creates the game handle
        self.game = game.Game()

        # If it finds the game, say so
        if self.game.hwnd is not None:
            print("LOCATED")
            self.form.isGameLocated.setText("Bookworm Adventures is located!")
        else:
            print("NOT LOCATED")

        # Adds events
        self.form.inputWord.clicked.connect(self.inputword_clicked)
        self.form.screenshotGrid.clicked.connect(self.screenshot_grid)
        self.form.readGrid.clicked.connect(self.readgrid_clicked)

        # Stores a list of english words, in tiles
        self.words = []
        f = open("resources/words.txt", "r")
        for line in f:
            self.words += [misc.string_to_tiles(line.rstrip())]
        f.close()

    def test(self):
        print("Test")

    # Screenshots the grid using either tesseract or pyautogui, then returns the screenshot
    def screenshot_grid(self):
        # Screenshots grid
        screenshot = self.game.screenshot_grid_filtered(int(self.form.tesseractThresholdSlider.value()))
        screenshot.save("screenshot.png")
        self.form.display.setPixmap(QtGui.QPixmap("screenshot.png"))

        # Returns grid
        return screenshot

    # Reads the grid using the screenshot with either tesseract or pyautogui
    def read_grid(self, screenshot):
        return self.game.get_letters_tesseract(screenshot) if self.form.radioTesseract.isChecked() \
            else self.game.get_letters_pyautogui(screenshot)

    # Displays a grid to the screen
    def display_grid(self, grid):
        # Clears box
        self.form.gridBox.setPlainText("")

        # Transposes grid for displaying
        grid = numpy.array(grid).transpose().tolist()

        # Goes through each row, putting in tiles
        for row in grid:
            for tile in row:
                self.form.gridBox.insertPlainText(
                    tile.upper() if tile is not None else "?"
                )
            self.form.gridBox.insertPlainText("\n")

    # ----------------
    # --* EVENTS
    # ----------------

    # When the read grid button is pressed
    def readgrid_clicked(self):
        # Screenshots grid and reads letters from grid
        grid = self.read_grid(self.screenshot_grid())

        # Displays grid
        self.display_grid(grid)

    # When the input word button is pressed
    def inputword_clicked(self):
        # Screenshots grid and reads letters from grid
        screenshot = self.screenshot_grid()
        grid = self.read_grid(screenshot)
        print(grid)

        # Displays grid
        self.display_grid(grid)

        # Thread function
        def thread_fun():

            # Puts all the letters into a full string
            full_str = ""

            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] is not None:
                        full_str += "qu" if grid[i][j] == "q" else grid[i][j]

            # Puts all the letters into a list of tiles
            tiles = misc.string_to_tiles(full_str)

            # Get a list of possible words
            possible_words = []
            for word in self.words:

                # If we can type this
                if misc.can_type(tiles, word):
                    possible_words += [word]

            # Sort words by length
            possible_words.sort(key=len)

            # Map each tile list to string
            possible_words = list(map(lambda tile_list: misc.tiles_to_string(tile_list), possible_words))

            # Reverses list of words, so biggest are at the front
            possible_words = possible_words[::-1]

            # -- DEBUG --
            top_words = possible_words[:10]
            for word in top_words:

                print("Typing out '" + word + "'...")

                positions = misc.string_to_pos(grid, word)

                self.game.focus()
                self.game.type(positions)

                sleep(1)

                if self.game.is_attack_enabled():
                    self.game.press_enter()
                    break
                else:
                    self.game.right_click()
                    sleep(0.25)

            print("Done!")
            # -----------

        # Starts a thread that does this
        thread = Thread(target=thread_fun)
        thread.start()
