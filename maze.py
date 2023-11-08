import random


class Maze_two:
    """
        Maze generating structure, which represents the walls as 1, and empty cells as 0
    """

    def __init__(self):
        self.wall = 1
        self.maze = []
        self.start_x, self.start_y = 0, 0
        self.maze_x, self.maze_y = 0, 0
        self.maze_end_x,self.maze_end_y = 0, 0

    def reset_maze(self):
        """
        generates a new blank grid of walls, clearing the old grid
        """
        self.maze = [[self.wall for i in range(self.maze_x)] for j in range(self.maze_y)]

    def frontiers(self, x, y):
        """
        Returns the frontiers of a cell, where a frontier are walls exactly 2 units from the cell
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: set of frontiers
        """
        f = set()
        if 0 <= x < self.maze_x and 0 <= y < self.maze_y:
            # west
            if x > 2 and self.maze[x - 2][y] == 1:
                f.add((x - 2, y))
            # east
            if x + 2 < self.maze_x - 1 and self.maze[x + 2][y] == 1:
                f.add((x + 2, y))
            # south
            if y > 2 and self.maze[x][y - 2] == 1:
                f.add((x, y - 2))
            # north
            if y + 2 < self.maze_y - 1 and self.maze[x][y + 2] == 1:
                f.add((x, y + 2))
        return f

    def neighbours(self, x, y):
        """
        Returns the neighbouring cells, where neighbours are 2 units from the cell and are passages.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: set of neighbouring cells
        """
        neighbours = set()
        if 0 <= x < self.maze_x and 0 <= y < self.maze_y:
            # west
            if x > 2 and self.maze[x - 2][y] == 0:
                neighbours.add((x - 2, y))
            # east
            if x + 2 < self.maze_x - 1 and self.maze[x + 2][y] == 0:
                neighbours.add((x + 2, y))
            # south
            if y > 1 and self.maze[x][y - 2] == 0:
                neighbours.add((x, y - 2))
            # north
            if y + 2 < self.maze_y - 1 and self.maze[x][y + 2] == 0:
                neighbours.add((x, y + 2))
        return neighbours

    def connect(self, x1, y1, x2, y2):
        """Sets both the frontier and cell between the frontier and origin cell to a passage
        :param x1: x coordinate of cell 1
        :param y1: y coordinate of cell 1
        :param x2: x coordinate of cell 2
        :param y2: y coordinate of cell 2
        """
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.maze[x1][y1] = 0
        self.maze[x][y] = 0

    def generate_maze(self, maze_x, maze_y):
        """
        Overview of the randomised Prim's frontier_set Algorithm:
        1 -> starting with a grid of  walls (represented by 1s)
        2 -> select a cell (x, y) and set it to a passage
        3 -> get the frontiers of this cell, and add it to frontier_set, a set of all frontiers
        4 -> loop whilst frontier_set is not empty: pick a random cell and remove it from frontier_set
        5 -> get neighbours of selected cell
        6 -> connect frontier (x,y) with a random neighbour neigbour_x,neighbour_y
        7 -> add the frontiers of the original frontier to frontier_set

        :return: completed maze, as a 2-dimensional array
        """
        self.maze_x = maze_x
        self.maze_y = maze_y
        self.reset_maze()

        frontier_set = set()
        x, y = (random.randint(1, self.maze_x - 1), random.randint(1, self.maze_y - 1))
        self.start_x, self.start_y = x, y

        self.maze[x][y] = 0
        cell_frontiers = self.frontiers(x, y)
        for frontier in cell_frontiers:
            frontier_set.add(frontier)
        while frontier_set:
            x, y = random.choice(tuple(frontier_set))
            frontier_set.remove((x, y))
            neighbour_set = self.neighbours(x, y)
            if neighbour_set:
                neigbour_x, neighbour_y = random.choice(tuple(neighbour_set))
                self.connect(x, y, neigbour_x, neighbour_y)
            cell_frontiers = self.frontiers(x, y)
            for frontier in cell_frontiers:
                frontier_set.add(frontier)

        self.set_maze_start()
        self.set_maze_end()
        return self.maze

    def is_passage(self, x, y):
        """
        Checks if a given cell is set to a passage
        :param x: x coordinate of cell
        :param y: y coordinate of cell
        :return: bool
        """
        return bool(self.maze[x][y] == 0)

    def get_maze_start(self):
        """
        Gets the SAFE maze startpoint
        :return: x, y coordinate of safe cell starting point
        """
        return self.start_x, self.start_y

    def get_maze_end(self):
        """
        Gets the SAFE maze endpoint
        :return: x, y coordinate of safe cell starting point
        """
        return self.maze_end_x, self.maze_end_y

    def set_maze_end(self):
        """
        algorithmn to define a valid endpoint for the maze:
        -> selects a cell opposite to the starting cell and selected a valid "passage" to occupy
        """
        x, y = self.get_maze_start()

        dist_to_x = self.maze_x - x
        dist_to_y = self.maze_y - y
        step_x = 0
        step_y = 0

        if dist_to_x < self.maze_x // 2:
            end_x = 2
            step_x += 1
        else:
            end_x = self.maze_x - 2
            step_x -= 1

        if dist_to_y < self.maze_y // 2:
            end_y = 2
            step_y += 1
        else:
            end_y = self.maze_x - 2
            step_y -= 1

        while not self.is_passage(end_x,end_y):
            next_x = end_x + step_x
            if self.is_passage(next_x, end_y):
                end_x = next_x
            else:
                next_y = end_y + step_y
                if self.is_passage(end_x, next_y):
                    end_y = next_y
            end_x += step_x
            end_y += step_y
        self.maze_end_x, self.maze_end_y = end_x, end_y
        self.maze[end_x][end_y] = 3


    def set_maze_start(self):
        """
        Locates a safe starting point for the player to be placed within the maze
        """
        dist_to_x = self.maze_x - self.start_x
        dist_to_y = self.maze_y - self.start_y
        step_x = 0
        step_y = 0

        if dist_to_x < self.maze_x // 2:
            step_x -= 1
        else:
            step_x += 1

        if dist_to_y < self.maze_y // 2:
            step_y -= 1
        else:
            step_y += 1

        while not self.is_passage(self.start_x, self.start_y):
            next_x = self.start_x + step_x
            if self.is_passage(next_x, self.start_y):
                self.start_x = next_x
            else:
                next_y = self.start_y + step_y
                if self.is_passage(self.start_x, next_y):
                    self.start_y = next_y
            self.start_x += step_x
            self.start_y += step_y
