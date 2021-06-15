# import pygame module
import pygame
# import drawing methods
import viewHelperMethods
# import PQ for A* pathfinding algorithm
from queue import PriorityQueue


# heuristic function for A* pathfinding algorithm
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance (L distance)


# A* pathfinding algorithm + real-time update of pygame window
def a_star_algorithm(draw, grid, start, end):
    # indexing variable for tracking WHEN the node was put into open_set,
    # used as tie breaker for when f_score of 2 or more nodes are equivalent
    index = 0
    # open set for algorithm
    open_set = PriorityQueue()
    # put start node with f_score of 0, index of 0
    open_set.put((0, index, start))
    # make a came_from dictionary that records where each node's "last node" was
    came_from = {}

    # initialize g_score dictionary with all nodes being mapped to infinity
    g_score = {node: float("inf") for row in grid for node in row}
    # set start node's g_score as 0, since distance from start node to itself is ofc 0
    g_score[start] = 0

    # initialize f_score dictionary with all nodes being mapped to infinity
    f_score = {node: float("inf") for row in grid for node in row}
    # set start node's f_score as heuristic function value from start node to end node
    f_score[start] = h(start.get_pos(), end.get_pos())

    # a set used as supplement to PQ, since PQ doesn't have method for checking if a node is in it or not
    open_set_hash = {start}

    # loop until open_set is not empty
    while not open_set.empty():
        # if X is pressed, then quit pygame - put here as safety measure against algorithm failure, etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get the next node with lowest f_score. if same score, python automatically gets the one with lower index value
        current = open_set.get()[2]
        # update open_set_hash to contain same set of nodes as open_set by removing current
        open_set_hash.remove(current)

        # if we just removed the end node, then we found the path
        if current == end:
            # draw path
            viewHelperMethods.reconstruct_path(came_from, end, draw)
            # mark end and start nodes, since reconstruct_path colors over them too
            end.make_end()
            start.make_start()
            # return that path is found
            return True

        # if what we removed isn't the end node, algo is still running.
        # get all neighbors of the current node
        for neighbor in current.neighbors:
            # get the possible g_score (shortest distance from start node to a given node) to current's neighbors
            # by adding 1 to it, since no edge is weighted in this scenario
            temp_g_score = g_score[current] + 1

            # if the possible g_score to current's neighbor is better/lower than current's neighbor's current g_score,
            # update neighbor's came_from node to current, and update g_score and f_score of neighbor
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                # if neighbor is not in open_set (open_set_hash used since set supports "not in"
                # this is where open_set_hash is used as supplement to open_set PQ
                if neighbor not in open_set_hash:
                    # increase index (variable for WHEN the node was put in open_set)
                    index += 1
                    # and then put the neighbor into open_set with new f_score, index
                    open_set.put((f_score[neighbor], index, neighbor))
                    # ... add to supplementary set as well
                    open_set_hash.add(neighbor)
                    # and set neighbor as open
                    neighbor.make_open()
        # update the window accordingly
        draw()

        # after considering all neighbors, close the node as visited if it isn't the start node
        if current != start:
            current.make_closed()

    # if this line is reached, that means there is no path from start to end, so return false
    return False
