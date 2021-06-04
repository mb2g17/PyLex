![logo](https://git.matt-barnes.co.uk/mb2g17/PyLex/raw/branch/master/resources/logo.png)

[![Available on GitHub](https://img.shields.io/badge/Available%20on-GitHub-white?style=flat-square&logo=github)](https://github.com/mb2g17/PyLex)

# What is this?
A python-based application that plays Bookworm Adventures.

It works by reading the screen and parsing the available letters based on the grid.

Then it will compute a list of possible words using the available letters, and will proceed to type out the words.

PyLex is compatible with both Volume 1 and Volume 2.

This uses libraries such as [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) for locating letters and inputting words, and [PyWin32](https://pypi.org/project/pywin32/) for locating the game window and fetching its position.

# Releases

https://git.matt-barnes.co.uk/mb2g17/PyLex/releases

# Setting up the project
## Prerequisites
To set up the project you will need:
 - Python 3.7
 - Pip
 - Virtualenv

## Setup

 1. Pull the repo and go into the repo
`git clone https://git.matt-barnes.co.uk/mb2g17/PyLex.git`
`cd PyLex`
 2. Create and activate a virtual environment
`virtualenv env`
`env\Scripts\activate`
 3. Install the requirements
`pip install -r requirements.txt`

## Running the project
To run PyLex, run the command:
`python main.py`
Make sure you've set up the project beforehand.
## Creating a distribution
To bundle the project in an executable, run:
`pyinstaller --onefile --windowed --icon=icon.ico --name=PyLex main.py`
If you get the error "Failed to execute script pyi_rth_pkgres", then run:
`pip uninstall pyinstaller`
`pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip`
... and try again.

# Developed with

Python 3.7.3

Windows 10 Education x64

# Images

![Screenshot1](https://git.matt-barnes.co.uk/mb2g17/PyLex/raw/branch/master/Screenshot_1.png)

![Screenshot2](https://git.matt-barnes.co.uk/mb2g17/PyLex/raw/branch/master/Screenshot_2.png)

![Screenshot3](https://git.matt-barnes.co.uk/mb2g17/PyLex/raw/branch/master/Screenshot_3.png)

# Videos

[![Demonstration_video](https://img.youtube.com/vi/g8HonXzjAeQ/0.jpg)](https://www.youtube.com/watch?v=g8HonXzjAeQ)