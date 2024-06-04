from StartScreen import StartScreen
from CheckersBoard import CheckersBoard

class MainWind:
    def __init__(self, root):
        self.root = root
        self.start_screen = StartScreen(root, self)

    def show_start_screen(self):
        self.start_screen = StartScreen(self.root, self)

    def start_checkers_game(self):
        self.checkers_board = CheckersBoard(self.root, self)
