import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
from settings import *
from map import *
from keyboard import *
import math as m
from raycast import *


class Player:
    """
    Handles all information and rendering of the player
    """

    def __init__(self, game):
        # Inherits the instance of the Game class
        self.game = game
        self.canvas = game.mini_map.map_display
        # Initialises the players starting position, angle, velocity
        start = maze.get_maze_start()
        self.player_x, self.player_y = start[1] * BLOCK_SIZE + 50, start[0] * BLOCK_SIZE + 50,
        self.player_angle = P_ANGLE
        self.player_velocity = P_VELOCITY

    def move(self):
        """
        Sets the players current velocity based on current facing direction and keys pressed
        :return:
        """
        cos_angle = m.cos(self.player_angle)
        sin_angle = m.sin(self.player_angle)
        x, y = (0, 0)
        x_vel = self.player_velocity * m.cos(self.player_angle)
        y_vel = self.player_velocity * m.sin(self.player_angle)
        keys = self.game.get_key()

        # Move Forward
        if "w" in keys:
            x += x_vel
            y += y_vel

        # Move Backwards
        if "s" in keys:
            x -= x_vel
            y -= y_vel

        # Strafe Left
        if "a" in keys:
            x += self.player_velocity * sin_angle
            y -= self.player_velocity * cos_angle

        # Strafe Right
        if "d" in keys:
            x -= self.player_velocity * sin_angle
            y += self.player_velocity * cos_angle

        # Rotate Left
        if "e" in keys:
            self.player_angle += PLAYER_SENSITIVITY

        # Rotate right
        if "q" in keys:
            self.player_angle -= PLAYER_SENSITIVITY

        if "z" in keys:
            x *= 4
            y *= 4

        self.check_collision(x, y)

    def draw_player(self):
        """
        Method renders the player onto the visualisation of the map within the map window
        """
        self.canvas.create_oval(self.player_x - 15, self.player_y - 15, self.player_x + 15,
                                self.player_y + 15, fill="red")
        self.canvas.create_line(self.player_x, self.player_y,
                                self.player_x + (50 * m.cos(self.player_angle)),
                                self.player_y + (50 * m.sin(self.player_angle)), fill="yellow",
                                width=3)
        if self.game.dev_mode:
            self.canvas.create_text(300, 50,
                                    text=f"x: {self.player_x} , y:{self.player_y}, rot:{self.player_angle}\n map: {self.get_map_pos()}",
                                    fill="black",
                                    font='Helvetica 15 bold')

    def check_wall(self, x, y):
        """
        Checks if a given cell is within the world map
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: bool if (x,y) in game map
        """
        if (x, y) not in self.game.mini_map.world_map:
            return True
        elif self.game.mini_map.world_map[x, y] == 3:
            return True

    def check_for_win(self):
        x, y = maze.get_maze_end()
        if self.get_map_pos() == (y, x):
            self.game.game_won = True

    def check_collision(self, x, y):
        """
        Collision detection whether the players coordinates reside within a cell in the map.
        -> Executes the players movement if no collisions detected
        :param x: x coordinate of player
        :param y: y coordinate of player
        """
        if self.check_wall(int((self.player_x + x) / BLOCK_SIZE), int(self.player_y / BLOCK_SIZE)):
            self.player_x += x
        if self.check_wall(int(self.player_x / BLOCK_SIZE), int((self.player_y + y) / BLOCK_SIZE)):
            self.player_y += y

    def get_pos(self):
        """
        Gets the players current position
        :return: x, y coordinates of the player
        """
        return self.player_x, self.player_y

    def get_map_pos(self):
        """
        Gets the players position in terms of which cell they are residing within
        :return: x, y coordinate of cell
        """
        return int((self.player_x) / BLOCK_SIZE), int((self.player_y) / BLOCK_SIZE)

    def update(self):
        """
        Calls the rendering of the player and movement of the player
        """
        self.draw_player()
        self.move()
        self.check_for_win()
