from PyQt5.QtWidgets import QPushButton

import misc


# A class that stores a list of words to use, as tiles
class Dictionary:

    # The list of words this dictionary holds
    words = []

    # The dictionary button handle
    button: QPushButton = None

    # Constructor
    def __init__(self, button):
        # Stores dictionary button handle
        self.button = button

    # Gets the words we're going to use
    def get_words(self):
        return self.words

    # Loads a file dictionary, given the path
    def load(self, path):
        # Stores a list of english words, in tiles
        self.words = []
        f = open(path, "r")
        for line in f:
            self.words += [misc.string_to_tiles(line.rstrip())]
        f.close()

        # Changes button text
        self.button.setEnabled(True)
        self.button.setText("Dictionary: " + path.split("/")[::-1][0])

    # Loads a dictionary based on volume
    # 1 - volume 1
    # 2 - volume 2
    def load_vol(self, vol):
        self.load("resources/words" + str(vol) + ".txt")
