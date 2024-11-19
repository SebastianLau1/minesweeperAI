import random
import numpy as np

class Minesweeper:
    """
    Minesweeper game representation
    """
    def __init__(self, height=16, width=16, mines=40):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = mines

        # Initialize an empty field with no mines
        self.board = np.zeros((height, width), dtype=int)
        self.mines_set = set()

        # Place mines randomly
        self.place_mines()

        # Initialize player knowledge
        self.visible = np.full((height, width), False, dtype=bool)

    def place_mines(self):
        """
        Randomly place mines on the board
        """
        mine_positions = random.sample(range(self.height * self.width), self.mines)
        for pos in mine_positions:
            row = pos // self.width
            col = pos % self.width
            self.board[row][col] = -1  # -1 represents a mine
            self.mines_set.add((row, col))

        # Calculate numbers for non-mine cells
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == -1:
                    continue
                self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        """
        Count the number of mines adjacent to a given cell
        """
        count = 0
        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.width, col + 2)):
                if (i, j) != (row, col) and self.board[i][j] == -1:
                    count += 1
        return count

    def is_mine(self, cell):
        return cell in self.mines_set

    def nearby_mines(self, cell):
        row, col = cell
        return self.board[row][col]

    def reveal(self, cell):
        self.visible[cell[0]][cell[1]] = True

    def is_visible(self, cell):
        return self.visible[cell[0]][cell[1]]
