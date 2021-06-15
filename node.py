# import pygame module
import pygame
# import constants
import constants


# Node object
class Node:
    # constructor
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = constants.UNVISITED
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # get position of node

    def get_pos(self):
        return self.row, self.col

    # getter functions

    def is_closed(self):
        return self.color == constants.CLOSED

    def is_open(self):
        return self.color == constants.OPEN

    def is_barrier(self):
        return self.color == constants.BARRIER

    def is_start(self):
        return self.color == constants.START

    def is_end(self):
        return self.color == constants.END

    # setter functions

    def reset(self):
        self.color = constants.UNVISITED

    def make_closed(self):
        self.color = constants.CLOSED

    def make_open(self):
        self.color = constants.OPEN

    def make_barrier(self):
        self.color = constants.BARRIER

    def make_start(self):
        self.color = constants.START

    def make_end(self):
        self.color = constants.END

    def make_path(self):
        self.color = constants.PATH

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # update neighbors of the node
    def update_neighbors(self, grid):
        # empty neighbor array
        self.neighbors = []

        # neighbor below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            # if not boundary node AND neighbor isn't barrier, add it
            self.neighbors.append(grid[self.row + 1][self.col])

        # neighbor above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            # if not boundary node AND neighbor isn't barrier, add it
            self.neighbors.append(grid[self.row - 1][self.col])

        # neighbor at left
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            # if not boundary node AND neighbor isn't barrier, add it
            self.neighbors.append(grid[self.row][self.col + 1])

        # neighbor at right
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            # if not boundary node AND neighbor isn't barrier, add it
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
