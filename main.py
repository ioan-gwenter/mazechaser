# Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
from threading import *
# Game File Imports
from settings import *
from map import *
from keyboard import *
from player import *
from timer import *
from menu import *
import os


# Game Class
class Game(Tk):
    """
    Top level class which inherits the instance of Tk inter. Holds the event loop for the program and handles
    all instances of supporting classes.
    """

    def __init__(self):
        # TopLevel Window
        super().__init__()
        self.title("RayCast Maze Game main window")
        self.geometry(f"{RES_WIDTH}x{RES_HEIGHT}")
        self.maxsize(RES_WIDTH, RES_HEIGHT)

        # Window Control
        self.game_running = True

        # Game Process Instances
        self.menu = Run_Menu(self)
        self.keyboard_input = KeyboardListener(self)
        self.mini_map = MiniMapViewer(self)
        self.player = Player(self)
        self.ray_cast = RayCast(self)

        # Canvas Widget
        self.display = Canvas()
        self.display.pack(fill="both", expand=True)
        self.display.focus_set()

        # Bindings
        self.bind("<Escape>", self.pause)
        self.bind("-", self.uber_cheat)
        self.bind("b", self.toggle_boss_key)
        self.bind("m", self.toggle_mini_map)
        self.bind("=", self.toggle_dev_mode)
        self.bind("<KeyPress>", self.keyboard_input.listener)
        self.bind("<KeyRelease>", self.keyboard_input.clear_pressed)

        # Game win conditions:
        self.game_won = False
        self.timer = object

        # sneaky secret things:
        self.dev_mode = False
        self.boss_key = False
        self.show_mini_map = False

    def init_timer(self):
        self.timer = Timer()

    def uber_cheat(self,event):
        x, y = maze.get_maze_end()
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.player.player_x, self.player.player_y = x, y

    def start_game(self):
        self.game_running = True
        self.run()

    def get_key(self):
        """
        Returns a list of currently pressed keys
        :return: list of key strings eg ["a"]
        """
        return self.keyboard_input.get_pressed()

    def toggle_boss_key(self, event):
        """
        toggles the boss key on and off
        :return:
        """
        self.boss_key = not self.boss_key

    def toggle_mini_map(self,event):
        self.show_mini_map = not self.show_mini_map

    def toggle_dev_mode(self,event):
        self.dev_mode = not self.dev_mode

    def pause(self, event):
        """
        Inverts the running state of the game
        :return:
        """

        self.game_running = not self.game_running

    def check_keyboard_events(self):
        """Handles any key-press driven events"""
        keys = self.get_key()

    def game_loop(self):
        """Contains the main running loop for the game"""

        # game dependent events
        if self.game_running:
            self.display.delete("all")
            self.mini_map.map_display.delete("all")
            self.timer.count()
            self.mini_map.draw_map()
            self.player.update()
            self.ray_cast.update()

            if self.game_won:
                self.timer.stop_clock()
                self.add_to_leaderboard()
                self.game_running = False
                self.destroy()
                self.quit()
                self.reset_game()

            if self.show_mini_map:
                self.mini_map.map_display.focus_set()
                self.mini_map.map_window.deiconify()
            else:
                self.display.focus_set()
                self.mini_map.map_window.withdraw()

        # menu dependent events
        self.check_keyboard_events()
        self.after(16, lambda: self.game_loop())

    def add_to_leaderboard(self):
        lb = open("leaderboard.txt",'a')
        score = f'{self.menu.player_name}, {self.timer.get_time()}\n'
        lb.write(score)
        lb.close()

    def run_menu(self):
        """Initialises the game loop and tkinter window when called"""
        self.withdraw()
        self.mini_map.map_window.withdraw()
        self.mainloop()

    def run(self):
        self.init_timer()
        self.mini_map.map_window.deiconify()
        self.deiconify()
        self.game_loop()
        self.mainloop()

    def reset_game(self):
        os.system('python3 run.py')

