import tkinter as tk
from CheckersPiece import CheckersPiece

class CheckersBoard:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.canvas = tk.Canvas(root, width=450, height=450)
        self.canvas.pack()
        self.selected_piece = None
        self.turn = "white"
        self.pieces = []
        self.captured_pieces = {"white": 0, "black": 0}
        self.create_board()
        self.create_pieces()
        self.canvas.bind("<Button-1>", self.click)

        self.new_game_button = tk.Button(root, text="Нова гра", command=self.back_to_start_screen)
        self.new_game_button.pack(side=tk.LEFT)
        self.restart_game_button = tk.Button(root, text="Перезапустити гру", command=self.restart_game)
        self.restart_game_button.pack(side=tk.RIGHT)

        self.turn_label = tk.Label(root, text=f"Зараз хід: {self.turn.capitalize()}")
        self.turn_label.pack()

        self.captured_label = tk.Label(root, text=f"Захоплені шашки - Білий: {self.captured_pieces['black']} "
                                                  f"Чорний: {self.captured_pieces['white']}")
        self.captured_label.pack()

    def create_board(self):
        colors = ["#DDB88C", "#A66D4F"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * 50 + 25
                y1 = row * 50 + 25
                x2 = x1 + 50
                y2 = y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        for i in range(8):
            self.canvas.create_text(15, i * 50 + 50, text=str(8 - i), font=("Arial", 12))
            self.canvas.create_text(i * 50 + 50, 15, text=chr(65 + i), font=("Arial", 12))

    def create_pieces(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.pieces.append(CheckersPiece(self.canvas, row, col, "white"))
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.pieces.append(CheckersPiece(self.canvas, row, col, "black"))

    def click(self, event):
        col = (event.x - 25) // 50
        row = (event.y - 25) // 50
        piece = self.get_piece(row, col)
        if self.selected_piece:
            if piece and piece.color == self.turn:
                self.selected_piece = piece
            elif self.selected_piece.valid_move(self, row, col):
                self.move_piece(self.selected_piece, row, col)
                if not self.selected_piece.check_additional_capture(self):
                    self.end_turn()
        elif piece and piece.color == self.turn:
            self.selected_piece = piece

    def get_piece(self, row, col):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def move_piece(self, piece, row, col):
        original_row, original_col = piece.row, piece.col
        piece.move(row, col)

        if abs(original_row - row) == 2:
            mid_row = (original_row + row) // 2
            mid_col = (original_col + col) // 2
            mid_piece = self.get_piece(mid_row, mid_col)
            if mid_piece:
                mid_piece.remove()
                self.pieces.remove(mid_piece)
                self.captured_pieces[piece.color] += 1
                self.update_captured_label()

        if (piece.color == "white" and row == 7) or (piece.color == "black" and row == 0):
            piece.crown()

    def must_capture(self, color):
        for piece in self.pieces:
            if piece.color == color:
                if piece.must_capture(self):
                    return True
        return False

    def end_turn(self):
        self.turn = "black" if self.turn == "white" else "white"
        self.turn_label.config(text=f"Зараз хід: {self.turn.capitalize()}")

    def update_captured_label(self):
        self.captured_label.config(
            text=f"Захоплені шашки - Білий: {self.captured_pieces['black']} Чорний: {self.captured_pieces['white']}")

    def back_to_start_screen(self):
        self.canvas.destroy()
        self.new_game_button.destroy()
        self.restart_game_button.destroy()
        self.turn_label.destroy()
        self.captured_label.destroy()
        self.app.show_start_screen()

    def restart_game(self):
        self.canvas.destroy()
        self.new_game_button.destroy()
        self.restart_game_button.destroy()
        self.turn_label.destroy()
        self.captured_label.destroy()
        self.__init__(self.root, self.app)
