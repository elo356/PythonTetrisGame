import time
from pygame.event import clear

from game.constants import COLUMNS, ROWS, LINE_CLEAR_SOUND

class Board:
    def __init__(self):
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]
        self.score = 0

    def is_valid_position(self, tetrimino, dx, dy, new_rotation=None):
        if new_rotation is None:
            new_rotation = tetrimino.rotation
        for y, row in enumerate(tetrimino.shape[new_rotation]):
            for x, cell in enumerate(row):
                if cell:
                    new_x = tetrimino.x + x + dx
                    new_y = tetrimino.y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def lock_piece(self, tetrimino):
        for y, row in enumerate(tetrimino.get_current_shape()):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[tetrimino.y + y][tetrimino.x + x] = tetrimino.color
        cleared_lines = self.clear_lines()
        # TODO TASK 8: Modify the score
        #   Score is defined as an increase of cleared_lines * 100
        if cleared_lines > 0:
            self.score += cleared_lines* 100
            LINE_CLEAR_SOUND.play()


    def clear_lines(self, row=0, cleared=0):
        # TODO TASK 7: Implement line clearing functionality.
        # Check each row to see if it is full (no empty spaces).
        # If a row is full, clear it and shift all rows above it down by one.
        # Keep track of how many lines are cleared and return the total number of cleared lines.
        # Use recursion to check and clear lines for all rows in the grid.
        if row >= ROWS:
            return cleared
        is_full_row = True
        for cell in self.grid[row]:
            if cell == 0:
                is_full_row = False
                break
        if is_full_row:
            self.grid[row].pop()
            self.grid.insert(0, [0] * COLUMNS)
            cleared += 1
            return self.clear_lines(row, cleared)
        else:
            return self.clear_lines(row + 1, cleared)
