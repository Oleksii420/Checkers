import tkinter as tk

class CheckersPiece:
    def __init__(self, canvas, row, col, color):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.id = self.create_piece()

    def create_piece(self):
        x1 = self.col * 50 + 30
        y1 = self.row * 50 + 30
        x2 = x1 + 40
        y2 = y1 + 40
        return self.canvas.create_oval(x1, y1, x2, y2, fill=self.color)

    def move(self, row, col):
        self.canvas.move(self.id, (col - self.col) * 50, (row - self.row) * 50)
        self.row = row
        self.col = col

    def crown(self):
        self.king = True
        self.canvas.itemconfig(self.id, fill="gold")

    def remove(self):
        self.canvas.delete(self.id)

    def valid_move(self, board, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False

        if not self.king:
            if self.color == "white" and row <= self.row:
                return False
            if self.color == "black" and row >= self.row:
                return False

            if abs(self.row - row) == 1 and abs(self.col - col) == 1 and not board.get_piece(row, col):
                return not board.must_capture(self.color)
            if abs(self.row - row) == 2 and abs(self.col - col) == 2:
                mid_row = (self.row + row) // 2
                mid_col = (self.col + col) // 2
                mid_piece = board.get_piece(mid_row, mid_col)
                if mid_piece and mid_piece.color != self.color and not board.get_piece(row, col):
                    return True

        else:
            if abs(self.row - row) == abs(self.col - col) and not board.get_piece(row, col):
                dr = (row - self.row) // abs(row - self.row)
                dc = (col - self.col) // abs(col - self.col)
                r, c = self.row + dr, self.col + dc
                while r != row and c != col:
                    mid_piece = board.get_piece(r, c)
                    if mid_piece:
                        if mid_piece.color == self.color:
                            return False
                        r += dr
                        c += dc
                        while r != row and c != col:
                            if board.get_piece(r, c):
                                return False
                            r += dr
                            c += dc
                        return True
                    r += dr
                    c += dc
                return not board.must_capture(self.color)

        return False

    def must_capture(self, board):
        for row_offset in [-2, 2]:
            for col_offset in [-2, 2]:
                row = self.row + row_offset
                col = self.col + col_offset
                if self.valid_move(board, row, col):
                    return True
        return False

    def check_additional_capture(self, board):
        for row_offset in [-2, 2]:
            for col_offset in [-2, 2]:
                row = self.row + row_offset
                col = self.col + col_offset
                if self.valid_move(board, row, col):
                    return True
        return False
