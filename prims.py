# A program which uses Prim's algorithm to generate a maze

import random
import numpy as np
import cv2


class Prims:

    def __init__(self, height, width, path, displayMaze):

        print("Using OpenCV version: " + cv2.__version__)

        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.path = path
        self.displayMaze = displayMaze

    def createMaze(self):
        maze = np.ones((self.height, self.width), dtype=float)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    maze[i, j] = 0.25

        sx = random.choice(range(2, self.height - 2, 2))
        sy = random.choice(range(2, self.width - 2, 2))

        self.prims(sx, sy, maze)

        for i in range(self.height):
            for j in range(self.width):
                if not maze[i, j] == 0:
                    maze[i, j] = 1

        maze[1, 2] = 1
        maze[self.height - 2, self.width - 3] = 1

        if self.displayMaze:
            cv2.namedWindow('Maze', cv2.WINDOW_NORMAL)
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        maze = maze * 255.0
        cv2.imwrite(self.path, maze)

        return 0

    def prims(self, x, y, grid):
        grid[y, x] = 0.5  # mark the starting cell as part of the maze

        # using a set might introcude bias to the maze
        adjacent = []

        if grid[y + 2, x] == 1:
            adjacent.append([y + 2, x])
        if grid[y - 2, x] == 1:
            adjacent.append([y - 2, x])
        if grid[y, x + 2] == 1:
            adjacent.append([y, x + 2])
        if grid[y, x - 2] == 1:
            adjacent.append([y, x - 2])

        while len(adjacent) > 0:

            # choose a random cell from the adjacent set
            cell = random.choice(adjacent)
            ny = cell[0]
            nx = cell[1]

            directions = []

            grid[ny, nx] = 0.5  # mark it as part of the maze

            # if the adjacant cells are part of the maze, crave a passage to one of them
            if grid[ny + 2, nx] == 0.5:
                directions.append(1)
            if grid[ny - 2, nx] == 0.5:
                directions.append(2)
            if grid[ny, nx + 2] == 0.5:
                directions.append(3)
            if grid[ny, nx - 2] == 0.5:
                directions.append(4)

            dir = random.choice(directions)

            if dir == 1:
                grid[ny + 1, nx] = 0.5
            elif dir == 2:
                grid[ny - 1, nx] = 0.5
            elif dir == 3:
                grid[ny, nx + 1] = 0.5
            elif dir == 4:
                grid[ny, nx - 1] = 0.5

            # if the adjacent cells are not part of the maze, add them to the set
            if grid[ny + 2, nx] == 1:
                adjacent.append([ny + 2, nx])
            if grid[ny - 2, nx] == 1:
                adjacent.append([ny - 2, nx])
            if grid[ny, nx + 2] == 1:
                adjacent.append([ny, nx + 2])
            if grid[ny, nx - 2] == 1:
                adjacent.append([ny, nx - 2])

            # remove any duplicates in the set
            adjacent = self.removeDuplicate(adjacent)

            adjacent.remove(cell)  # reomve the cell from the set

    def removeDuplicate(self, _list):
        final_list = []
        for num in _list:
            if num not in final_list:
                final_list.append(num)
        return final_list
