import tkinter as tk

class StartScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Виберіть тип гри")
        self.label.pack()
        self.local_game_button = tk.Button(self.frame, text="Гра на одному пристрої", command=self.start_local_game)
        self.local_game_button.pack()

    def start_local_game(self):
        self.frame.destroy()
        self.app.start_checkers_game()
