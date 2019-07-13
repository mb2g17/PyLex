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
    # Tile scores
    tile_score = {
        "a": 1,
        "b": 1.25,
        "c": 1.25,
        "d": 1,
        "e": 1,
        "f": 1.25,
        "g": 1,
        "h": 1.25,
        "i": 1,
        "j": 1.75,
        "k": 1.75,
        "l": 1,
        "m": 1.25,
        "n": 1,
        "o": 1,
        "p": 1.25,
        "q": 1.75,
        "r": 1,
        "s": 1,
        "t": 1,
        "u": 1,
        "v": 1.5,
        "w": 1.5,
        "x": 2,
        "y": 1.5,
        "z": 2,
    }

    # The possible words to type in
    words = []

    # Constructor; adds view to window
    def __init__(self, window):

        # Creates the view
        self.form = form_view.Ui_Form()
        self.form.setupUi(window)

        # Creates the game handle
        self.game = game.Game()

        # If it finds the game
        if self.game.hwnd is not None:
            # If it's volume 1
            if self.game.version == 1:
                self.form.isGameLocated.setText("Bookworm Adventures is located!")
                self.load_words(1)
            # If it's volume 2
            elif self.game.version == 2:
                self.form.isGameLocated.setText("Bookworm Adventures Vol. 2 is located!")
                self.load_words(2)
            else:
                self.load_words(1)

            # Make the text green
            self.form.isGameLocated.setStyleSheet("color:darkgreen;background-color:rgb(191, 255, 187);")

        # Adds events
        self.form.inputWord.clicked.connect(self.inputword_clicked)
        self.form.screenshotGrid.clicked.connect(self.screenshotgrid_clicked)
        self.form.readGrid.clicked.connect(self.readgrid_clicked)
        self.form.getPossibleWords.clicked.connect(self.getpossiblewords_clicked)

    def test(self):
        print("Test")

    # Loads words, vol=1 for the first game, vol=2 for the second
    def load_words(self, vol):
        # Stores a list of english words, in tiles
        self.words = []
        f = open("resources/words" + str(vol) + ".txt", "r")
        for line in f:
            self.words += [misc.string_to_tiles(line.rstrip())]
        f.close()

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
                    tile.upper() if tile is not None else "#"
                )
            self.form.gridBox.insertPlainText("\n")

    # Gets possible words given a grid
    def get_possible_words(self, grid):
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

        # Map each tile list to string
        possible_words = list(map(lambda tile_list: misc.tiles_to_string(tile_list), possible_words))

        # Sorts words
        possible_words = self.sort_word_list(possible_words)

        # Return list of possible words
        return possible_words

    # Gets a word's score
    def get_word_score(self, word):
        return sum(
            list(
                map(lambda c: self.tile_score[c], word)
            )
        )

    # Sorts a word list
    def sort_word_list(self, word_list):

        # If we're doing it by score
        if self.form.radioSortByScore.isChecked():
            # Sorts by score
            word_list.sort(key=lambda word: self.get_word_score(word), reverse=True)
        else:
            # Sorts by length
            word_list.sort(key=len, reverse=True)

        # Return new list
        return word_list

    # ----------------
    # --* EVENTS
    # ----------------

    # When the screenshot grid button is pressed
    def screenshotgrid_clicked(self):
        # Screenshots grid
        self.screenshot_grid()

        # Erase grid box and possible word box
        self.form.gridBox.setPlainText("")
        self.form.possibleWordsBox.setPlainText("")

    # When the read grid button is pressed
    def readgrid_clicked(self):
        # Screenshots grid and reads letters from grid
        grid = self.read_grid(self.screenshot_grid())

        # Displays grid
        self.display_grid(grid)

        # Erase possible word box
        self.form.possibleWordsBox.setPlainText("")

    # When the get possible words button is pressed
    def getpossiblewords_clicked(self):
        # Gets a list of possible words
        grid = self.read_grid(self.screenshot_grid())
        possible_words = self.get_possible_words(grid)

        # Displays grid
        self.display_grid(grid)

        # Gets top words
        top_words = possible_words[:self.form.wordsToTrySpinBox.value()]

        # Puts them in box
        self.form.possibleWordsBox.setPlainText("")
        for word in top_words:
            self.form.possibleWordsBox.insertPlainText(word + "\n")

    # When the input word button is pressed
    def inputword_clicked(self):
        # Screenshots grid and reads letters from grid
        screenshot = self.screenshot_grid()
        grid = self.read_grid(screenshot)
        print(grid)

        # Displays grid
        self.display_grid(grid)

        # Gets a list of possible words
        possible_words = self.get_possible_words(grid)

        # Gets top words and puts them in box
        top_words = possible_words[:self.form.wordsToTrySpinBox.value()]
        self.form.possibleWordsBox.setPlainText("")
        for word in top_words:
            self.form.possibleWordsBox.insertPlainText(word + "\n")

        # Thread function
        def thread_fun():

            # Writes out top words
            for word in top_words:

                print("Typing out '" + word + "'...")

                # Converts words to positions on the grid
                positions = misc.string_to_pos(grid, word)

                # Focus on the game, and type the word out
                self.game.focus()
                self.game.type(positions)

                # Wait for the animations to play
                sleep(1)

                # If the attack button is enabled, submit. If not, erase and start again
                if self.game.is_attack_enabled():
                    self.game.press_enter()
                    break
                else:
                    self.game.right_click()
                    sleep(0.25)

            print("Done!")

        # Starts a thread that does this
        thread = Thread(target=thread_fun)
        thread.start()
