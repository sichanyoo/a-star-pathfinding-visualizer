# import pygame module
import pygame
# import constants, node class, pathfinding algorithm methods, and view helper methods that draw elements
import constants
import node
import pathfindingAlgo
import viewHelperMethods

############################################################################################################
############################################################################################################
# PYGAME WINDOW #

# visualizer window as square, 800x800 pixel
WIN = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))
# visualizer window caption
pygame.display.set_caption("A* Path Finding Algorithm Visualizer")


############################################################################################################
############################################################################################################
# HELPER METHODS #

# this method makes 2D array (grid) of size [rows][rows] of Node objects
def make_grid(rows, width):
    grid = []
    # width/height of each node on pygame window
    gap = width // rows

    # make list[list[Node]]
    for i in range(rows):
        row = []
        for j in range(rows):
            row.append(node.Node(i, j, gap, rows))
        grid.append(row)

    return grid


# this method returns [x][y] indices of the node that was clicked
def get_clicked_pos(pos, rows, width):
    # get width/height of each node on pygame window
    gap = width // rows

    # get [x][y] indices of node that was clicked, by dividing actual mouse coordinate by gap
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col

############################################################################################################
############################################################################################################
# main method #


def main(win, width):
    # number of nodes on square window
    rows = 50
    # get 2D grid of nodes
    grid = make_grid(rows, width)

    # start / end node variables
    start = None
    end = None

    # app while loop variable
    run = True
    # variables used to prevent user from starting A* pathfinding algorithm without resetting the window
    started = False
    finished = False

    while run:
        # draw over the whole grid
        viewHelperMethods.draw(win, grid, rows, width)
        # for all event gathered since last iteration
        for event in pygame.event.get():
            # if X clicked on window, stop running program
            if event.type == pygame.QUIT:
                run = False

            # if algorithm is started and on-going, skip over to next iteration of for loop
            if started and not finished:
                continue

            # if left mouse button is clicked:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # get the clicked node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]

                # if start node hasn't been placed AND clicked node isn't the end node, make it start node
                if not start and node != end:
                    start = node
                    start.make_start()
                # if end node hasn't been placed AND clicked node isn't the start node, make it end node
                elif not end and node != start:
                    end = node
                    end.make_end()
                # in neither case, make the node a barrier
                elif node != end and node != start:
                    node.make_barrier()

            # if right mouse button is clicked:
            elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                # get the clicked node, then make it white
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()

                # then, if the clicked node was start/end, reset start/end variables
                if node == start:
                    start = None
                if node == end:
                    end = None

            # if a key on keyboard was pressed
            if event.type == pygame.KEYDOWN:
                # if it was space bar AND start/end nodes have been set AND algorithm hasn't been run since last reset
                if event.key == pygame.K_SPACE and start and end and not started:
                    # for all nodes on grid, update their neighbors
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    # set these to true so user can't restart algorithm before resetting the pygame window first
                    started = True
                    finished = True
                    # show A* pathfinding algorithm
                    pathfindingAlgo.a_star_algorithm(lambda: viewHelperMethods.draw(win, grid, rows, width), grid, start, end)

                # if it was 'c' key, then reset the pygame window, and all other variables accordingly
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    finished = False
                    started = False
                    # remake grid to reset it
                    grid = make_grid(rows, width)

    # reaching this point means program exited while loop, then time to close the pygame.
    pygame.quit()

############################################################################################################
############################################################################################################
# app entry #


main(WIN, constants.WIDTH)
