import form_controller

from PyQt5 import QtWidgets

# Initialises the app
app = QtWidgets.QApplication([])
app.setStyle("Fusion")

# Creates window
window = QtWidgets.QWidget()

# Sets up form for window
form = form_controller.UiController(window)

# Shows window and executes app
window.show()
app.exec_()
