# Imports
from maze import *
from settings import *
from tkinter import *

# Game Map Instance
maze = Maze_two()
game_map = maze.generate_maze(21, 21)

game_map_width = len(game_map)
game_map_height = len(game_map)


class MiniMapViewer():
    def __init__(self, game):
        """
        Map Data Structure. Used to render the map and handle the map window

        :param game: instance of the Game class
        """

        # Window initialisation
        self.map_window = Toplevel(game)
        self.game = game
        self.map_window.title("Map Viewer")
        self.map_window.geometry(f"{game_map_width * BLOCK_SIZE}x{game_map_height * BLOCK_SIZE}")

        # Canvas initialisation
        self.map_display = Canvas(self.map_window, bg="white")
        self.map_display.pack(fill="both", expand=True)

        # Mouse Binding
        self.map_display.bind("<ButtonPress-1>", self.scroll_start)
        self.map_display.bind("<B1-Motion>", self.scroll_move)

        # World map handling
        self.world_map = {}
        self.create_map()

        self.map_display.bind("m", self.game.toggle_mini_map)
        self.map_window.protocol("WM_DELETE_WINDOW",self.game.quit)

    def close_window(self):
        self.map_window.destroy()

    def create_map(self):
        """
        Method adds any occupied map spaces to a dictionary, holding (x,y) of the cell and the wall type
        """
        for row, map_row in enumerate(game_map):
            for col, wall_type in enumerate(map_row):
                block_x, block_y = col * BLOCK_SIZE, row * BLOCK_SIZE
                if wall_type != 0:
                    self.world_map[(col, row)] = wall_type

    def draw_map(self):
        """
        Draws all cells within world map onto the canvas
        """
        for block in self.world_map:
            if self.world_map[block] == 3:
                colour = "green"
            else:
                colour = "blue"
            self.map_display.create_rectangle(block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE,
                                              block[0] * BLOCK_SIZE + BLOCK_SIZE, block[1] * BLOCK_SIZE + BLOCK_SIZE,
                                              fill=colour, outline="white")

    def scroll_start(self, event):
        """
        Triggers a scroll event on the canvas
        """
        self.map_display.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        """
        Scrolls the canvas to the location of the mouse
        :return:
        """
        self.map_display.scan_dragto(event.x, event.y, gain=1)
