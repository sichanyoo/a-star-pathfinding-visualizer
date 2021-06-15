# import pygame module
import pygame
# import constants
import constants


# function to draw grid lines
def draw_gridlines(win, rows, width):
    # distance between gridlines (i.e., width/height of each node square)
    gap = width // rows
    for i in range(rows):
        # horizontal lines
        pygame.draw.line(win, constants.GRID_LINE, (0, i * gap), (width, i * gap))
        # vertical lines
        pygame.draw.line(win, constants.GRID_LINE, (i * gap, 0), (i * gap, width))


# draw the pygame window
def draw(win, grid, rows, width):
    win.fill(constants.UNVISITED)

    # draw all nodes on pygame window
    for row in grid:
        for node in row:
            node.draw(win)

    # draw gridlines
    draw_gridlines(win, rows, width)

    # show the window
    pygame.display.update()


# color the path
def reconstruct_path(came_from, current, draw_lambda):
    # this while loop stops eventually since came_from of start node is none and won't be in came_from anymore
    while current in came_from:
        # get the last node of current
        current = came_from[current]
        # color it as path
        current.make_path()
        # update window
        draw_lambda()
