from PyQt5 import QtGui

import form_view
import game


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

    # When the input word button is pressed
    def inputword_clicked(self):

        # Screenshots grid
        screenshot = self.game.screenshot_grid()
        screenshot.save("screenshot.png")
        self.form.display.setPixmap(QtGui.QPixmap("screenshot.png"))

        # Reads letters from grid
        grid = self.game.get_letters(screenshot)

        # Compiles

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                print(grid[i][j], end='')

        # -----------
